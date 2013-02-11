# -*- coding: utf-8 -*-

from django.core import management
from apps.registration.models import RegistrationProfile
from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import datetime
from django.conf import settings


class RegistrationManagementTestCase(TestCase):
    user_info = {'username': 'wangchao3',
                 'password': '1q2w3e4r',
                 'email': '4reg@xsudo.com'}
    def test_management_command(self):
        """
        测试调用命令行工具 删除过期 没有激活的用户
        """
        new_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                    **self.user_info)
        expired_user = RegistrationProfile.objects.create_inactive_user(site=Site.objects.get_current(),
                                                                        username='bob',
                                                                        password='secret',
                                                                        email='bob@example.com')
        expired_user.date_joined -= datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        expired_user.save()

        management.call_command('cleanupregistration')
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertRaises(User.DoesNotExist, User.objects.get, username='bob')
