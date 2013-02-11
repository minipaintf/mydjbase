# -*- coding: utf-8 -*-
"""
2013-02-09
视图层的测试
"""
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from apps.registration import forms
from apps.registration.models import RegistrationProfile


class RegistrationViewTests(TestCase):
    """
    Test the registration views.

    """
    urls = 'apps.registration.tests.urls'

    def setUp(self):
        """
        设置激活的过期时间
        """
        self.old_activation = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', None)
        if self.old_activation is None:
            settings.ACCOUNT_ACTIVATION_DAYS = 7 # pragma: no cover

    def tearDown(self):
        """
        复位激活过期时间
        """
        if self.old_activation is None:
            settings.ACCOUNT_ACTIVATION_DAYS = self.old_activation # pragma: no cover

    def test_registration_view_initial(self):
        """
        注册页面的初始化
        """
        response = self.client.get(reverse('registration_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'registration/registration_form.html')
        self.assertTrue(isinstance(response.context['form'],
                                   forms.RegisterForm))

    def test_registration_view_success(self):
        """
        成功注册,来到注册成功的页面
        """
        response = self.client.post(reverse('registration_register'),
                                    data={'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish'})
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('registration_complete'))
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_registration_view_failure(self):
        """
        测试注册失败,错误信息的返回值 两次输入密码不一致
        """
        response = self.client.post(reverse('registration_register'),
                                    data={'username': 'bob',
                                          'email': 'bobe@example.com',
                                          'password1': 'foo',
                                          'password2': 'bar'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field='password2',
                             errors=u'两个密码字段不一致。')
        self.assertEqual(len(mail.outbox), 0)

    def test_registration_view_closed(self):
        """
        注册关闭的测试
        """
        old_allowed = getattr(settings, 'REGISTRATION_OPEN', True)
        settings.REGISTRATION_OPEN = False

        closed_redirect = 'http://testserver%s' % reverse('registration_disallowed')

        response = self.client.get(reverse('registration_register'))
        self.assertRedirects(response, closed_redirect)

        # Even if valid data is posted, it still shouldn't work.
        response = self.client.post(reverse('registration_register'),
                                    data={'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish'})
        self.assertRedirects(response, closed_redirect)
        self.assertEqual(RegistrationProfile.objects.count(), 0)

        settings.REGISTRATION_OPEN = old_allowed

    def test_registration_template_name(self):
        """
        Passing ``template_name`` to the ``register`` view will result
        in that template being used.

        """
        response = self.client.get(reverse('registration_test_register_template_name'))
        self.assertTemplateUsed(response,
                                'registration/test_template_name.html')

    def test_registration_extra_context(self):
        """
        测试注册的时候带入额外的变量
        """
        response = self.client.get(reverse('registration_test_register_extra_context'))
        self.assertEqual(response.context['foo'], 'bar')
        # Callables in extra_context are called to obtain the value.
        self.assertEqual(response.context['callable'], 'called')

    def test_registration_disallowed_url(self):
        """
        测试不允许注册的时候 定义好不允许注册的url,然后验证返回的url是否就是这个
        """
        old_allowed = getattr(settings, 'REGISTRATION_OPEN', True)
        settings.REGISTRATION_OPEN = False

        closed_redirect = 'http://testserver%s' % reverse('registration_test_custom_disallowed')

        response = self.client.get(reverse('registration_test_register_disallowed_url'))
        self.assertRedirects(response, closed_redirect)

        settings.REGISTRATION_OPEN = old_allowed

    def test_registration_success_url(self):
        """
        测试当传入注册成的返回url的时候的返回链接
        """
        success_redirect = 'http://testserver%s' % reverse('registration_test_custom_success_url')
        response = self.client.post(reverse('registration_test_register_success_url'),
                                    data={'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish'})
        self.assertRedirects(response, success_redirect)

    def test_valid_activation(self):
        """
        测试激活一个合法的成功验证
        """
        success_redirect = 'http://testserver%s' % reverse('registration_activation_complete')
        
        # First, register an account.
        self.client.post(reverse('registration_register'),
                         data={'username': 'alice',
                               'email': 'alice@example.com',
                               'password1': 'swordfish',
                               'password2': 'swordfish'})
        profile = RegistrationProfile.objects.get(user__username='alice')
        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key': profile.activation_key}))
        self.assertRedirects(response, success_redirect)
        self.failUnless(User.objects.get(username='alice').is_active)

    def test_invalid_activation(self):
        """
        测试一个非法的激活操作,已经过期的激活码不能激活
        """
        # Register an account and reset its date_joined to be outside
        # the activation window.
        self.client.post(reverse('registration_register'),
                         data={'username': 'bob',
                               'email': 'bob@example.com',
                               'password1': 'secret',
                               'password2': 'secret'})
        expired_user = User.objects.get(username='bob')
        expired_user.date_joined = expired_user.date_joined - datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        expired_user.save()

        expired_profile = RegistrationProfile.objects.get(user=expired_user)
        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key': expired_profile.activation_key}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['activation_key'],
                         expired_profile.activation_key)
        self.assertFalse(User.objects.get(username='bob').is_active)

    def test_activation_success_url(self):
        """
        测试激活成功的时候,传入成功的返回地址,然后验证是否正确的返回到这个url
        """
        success_redirect = 'http://testserver%s' % reverse('registration_test_custom_success_url')
        self.client.post(reverse('registration_register'),
                         data={'username': 'alice',
                               'email': 'alice@example.com',
                               'password1': 'swordfish',
                               'password2': 'swordfish'})
        profile = RegistrationProfile.objects.get(user__username='alice')
        response = self.client.get(reverse('registration_test_activate_success_url',
                                           kwargs={'activation_key': profile.activation_key}))
        self.assertRedirects(response, success_redirect)
        
    def test_activation_template_name(self):
        """
        测试传入模板名字的
        """
        response = self.client.get(reverse('registration_test_activate_template_name',
                                   kwargs={'activation_key': 'foo'}))
        self.assertTemplateUsed(response, 'registration/test_template_name.html')

    def test_activation_extra_context(self):
        """
        测试激活的时候,在相应的时候传入额外的变量
        """
        response = self.client.get(reverse('registration_test_activate_extra_context',
                                           kwargs={'activation_key': 'foo'}))
        self.assertEqual(response.context['foo'], 'bar')
        # Callables in extra_context are called to obtain the value.
        self.assertEqual(response.context['callable'], 'called')
