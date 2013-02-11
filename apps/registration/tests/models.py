# -*- coding: utf-8 -*-
"""
测试注册的model
create date: 2013-02-07
"""
import datetime
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase
from django.utils.hashcompat import sha_constructor

from apps.registration.models import RegistrationProfile


class RegistrationModelTests(TestCase):
    """
    Test the model and manager used in the default backend.
    
    """
    user_info = {'username': 'wangchao3',
                 'password': '1q2w3e4r',
                 'email': '4reg@xsudo.com'}
    
    def setUp(self):
        self.old_activation = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', None)
        settings.ACCOUNT_ACTIVATION_DAYS = 7

    def tearDown(self):
        settings.ACCOUNT_ACTIVATION_DAYS = self.old_activation

    def test_profile_creation(self):
        """
        测试创建用户的时候创建用户的激活码,包括激活码是否规范
        """
        new_user = User.objects.create_user(**self.user_info)
        profile = RegistrationProfile.objects.create_profile(new_user)

        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(profile.user.id, new_user.id)
        self.assertTrue(re.match('^[a-f0-9]{40}$', profile.activation_key))
        self.assertEqual(unicode(profile),
                         "Registration information for wangchao3")

    def test_activation_email(self):
        """
        测试发送了激活码邮件        
        """
        new_user = User.objects.create_user(**self.user_info)
        profile = RegistrationProfile.objects.create_profile(new_user)
        profile.send_activation_email(Site.objects.get_current())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])

    def test_user_creation(self):
        """
        测试用户创建
        """
        new_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                    **self.user_info)
        self.assertEqual(new_user.username, 'wangchao3')
        self.assertEqual(new_user.email, '4reg@xsudo.com')
        self.assertTrue(new_user.check_password('1q2w3e4r'))
        self.assertFalse(new_user.is_active)

    def test_user_creation_email(self):
        """
        测试邮件创建发送成功
        """
        new_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                    **self.user_info)
        self.assertEqual(len(mail.outbox), 1)

    def test_user_creation_no_email(self):
        """
        测试不发送邮件的方法
        """
        new_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                    send_email=False,
                                                                    **self.user_info)
        self.assertEqual(len(mail.outbox), 0)

    def test_unexpired_account(self):
        """
        测试验证码未过期
        """
        new_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                    **self.user_info)
        profile = RegistrationProfile.objects.get(user=new_user)
        self.assertFalse(profile.activation_key_expired())

    def test_expired_account(self):
        """
        测试验证码过期,在设定时间加上一天
        """
        new_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                    **self.user_info)
        new_user.date_joined -= datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        new_user.save()
        profile = RegistrationProfile.objects.get(user=new_user)
        self.assertTrue(profile.activation_key_expired())

    def test_valid_activation(self):
        """
        测试成功的账户激活
        """
        new_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                    **self.user_info)
        profile = RegistrationProfile.objects.get(user=new_user)
        activated = RegistrationProfile.objects.activate_user(profile.activation_key)

        self.assertTrue(isinstance(activated, User))
        self.assertEqual(activated.id, new_user.id)
        self.assertTrue(activated.is_active)

        profile = RegistrationProfile.objects.get(user=new_user)
        self.assertEqual(profile.activation_key, RegistrationProfile.ACTIVATED)

    def test_expired_activation(self):
        """
        测试过期了的激活
        """
        new_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                    **self.user_info)
        new_user.date_joined -= datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        new_user.save()

        profile = RegistrationProfile.objects.get(user=new_user)
        activated = RegistrationProfile.objects.activate_user(profile.activation_key)

        self.assertFalse(isinstance(activated, User))
        self.assertFalse(activated)

        new_user = User.objects.get(username='wangchao3')
        self.assertFalse(new_user.is_active)

        profile = RegistrationProfile.objects.get(user=new_user)
        self.assertNotEqual(profile.activation_key, RegistrationProfile.ACTIVATED)

    def test_activation_invalid_key(self):
        """
        测试无效的激活码激活  这个根本不符合验证码的正则表达式
        """
        self.assertFalse(RegistrationProfile.objects.activate_user('foo'))

    def test_activation_already_activated(self):
        """
        测试去激活已经激活过了的
        """
        new_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                    **self.user_info)
        profile = RegistrationProfile.objects.get(user=new_user)
        RegistrationProfile.objects.activate_user(profile.activation_key)

        profile = RegistrationProfile.objects.get(user=new_user)
        self.assertFalse(RegistrationProfile.objects.activate_user(profile.activation_key))

    def test_activation_nonexistent_key(self):
        """
        测试激活不存在的激活码
        """
        # Due to the way activation keys are constructed during
        # registration, this will never be a valid key.
        invalid_key = sha_constructor('foo').hexdigest()
        self.failIf(RegistrationProfile.objects.activate_user(invalid_key))

    def test_expired_user_deletion(self):
        """
        测试过期的用户删除
        """
        new_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                    **self.user_info)
        expired_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                        username='bob',
                                                                        password='secret',
                                                                        email='bob@example.com')
        expired_user.date_joined -= datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        expired_user.save()

        RegistrationProfile.objects.delete_expired_users()
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertRaises(User.DoesNotExist, User.objects.get, username='bob')