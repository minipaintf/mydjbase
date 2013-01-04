# -*- coding: utf-8 -*-
"""
2013-01-03
注册的业务测试
"""


from django.test import TestCase
from django.test.client import Client
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class RegisterTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(RegisterTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(RegisterTest, cls).tearDownClass()

    # 测试注册页面
    def test_register_view(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/sign_up/'))
        # title
        self.assertIn("注册", self.selenium.title)
        # 跨域提交
        self.assertIsNotNone(self.selenium.find_element_by_name("csrfmiddlewaretoken"))
        # email
        email_input = self.selenium.find_element_by_name("email")
        self.assertIsNotNone(email_input)
        email_input.send_keys('wangchao@xsudo.com')
        # 用户名
        username_input = self.selenium.find_element_by_name("username")
        self.assertIsNotNone(username_input)
        username_input.send_keys('wangchao')
        # 密码
        password_input = self.selenium.find_element_by_name("password1")
        self.assertIsNotNone(password_input)
        password_input.send_keys('1q2w3e4r')
        # 密码确认
        password_confirm_input = self.selenium.find_element_by_name("password2")
        self.assertIsNotNone(password_confirm_input)
        password_confirm_input.send_keys('1q2w3e4r')
        #password_input.send_keys(Keys.RETURN)
        # 注册按钮
        submit_button = self.selenium.find_element_by_tag_name("button")
        self.assertIsNotNone(submit_button)
        #submit_button.click()

    # 测试注册失败
    def test_register_error(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/sign_up/'))
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys('wangchao@xiaoma.com')
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('vincent')
        password_input = self.selenium.find_element_by_name("password1")
        password_input.send_keys('1q2w3e4r')
        password_confirm_input = self.selenium.find_element_by_name("password2")
        password_confirm_input.send_keys('1q2w3e4r_asjdhkja')
        submit_button = self.selenium.find_element_by_tag_name("button")
        submit_button.click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('此邮箱已经存在', body.text)
        self.assertIn('已存在一位使用该名字的用户', body.text)
        self.assertIn('两个密码字段不一致', body.text)

    # 测试注册成功
    def test_register_success(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/sign_up/'))
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys('wangchao2@xiaoma.com')
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('vincent2')
        password_input = self.selenium.find_element_by_name("password1")
        password_input.send_keys('1q2w3e4r')
        password_confirm_input = self.selenium.find_element_by_name("password2")
        password_confirm_input.send_keys('1q2w3e4r')
        submit_button = self.selenium.find_element_by_tag_name("button")
        submit_button.click()
        body = self.selenium.find_element_by_tag_name('body')
        
        current_url = self.selenium.current_url
        current_url_ex = '%s%s' % (self.live_server_url, '/')
        self.assertEqual(current_url_ex, current_url)

        # 验证数据库里已经成功存在此用户
        user = User.objects.get(username='vincent2')
        self.assertIsNotNone(user)
        #self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)
        # 验证可以登录
        user2 = authenticate(username='vincent2', password='1q2w3e4r')
        self.assertIsNotNone(user2)



















