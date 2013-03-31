# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase



class UcenterViewTests(TestCase):
    """
    Test the ucenter views.

    """
    #urls = 'apps.registration.tests.urls'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_registration_view_initial(self):
        """
        注册页面的初始化
        """
        response = self.client.get(reverse('api_uc_php'))
        self.assertEqual(response.status_code, 200)
