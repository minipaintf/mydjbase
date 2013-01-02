# -*- coding: utf-8 -*-
"""
2012-12-23 
"""

from django.test import TestCase
from django.test.client import Client
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys


class IndexViewTest(TestCase):
    def test_index_view(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('firstp/index.html')
        # title里有任务列表
        self.assertContains(response,
            '<title>首页 - 网络组内部业务系统</title>',
            status_code=200)


# 首页的测试
class todosIndexViewTest(TestCase):
    def test_todos_view_index(self):
        """
        打开首页的时候,应该看见"任务列表",和新建任务.
        """
        c = Client()
        response = c.get('/todos/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('todos/index.html')
        # title里有任务列表
        self.assertContains(response,
            '<title>首页 - 任务列表 - 网络组内部业务系统</title>',
            status_code=200)
# 测试登录的流程
class loginTestCase(TestCase):
    """
    the page have login form
    """
    fixtures = ['initial_data.json']
    def test_login_form(self):
        c = Client()
        response = c.get('/')
        # 有登录按钮
        self.assertContains(response, '登录')
        
        self.assertContains(response, 'name="username"')
        # 登录错误 跳转到登录页面
        response = c.post('/accounts/login/', {'username': 'john', 'password': 'smith'})
        self.assertTemplateUsed('/registration/login.html')
        # self.assertRedirects(response, '/accounts/login/')
        self.assertEqual(response.status_code, 200)
        # 测试登录的另一种方法
        #print c.login(username='vincent', password='1q2w3e4r')
        # self.assertTrue(login)

        # 正确登录 跳转到首页
        #response = c.get('/accounts/login/')
        # print response
        response = c.post('/accounts/login/', {'username': 'vincent', 'password': '1q2w3e4r'})
        #print response
        # self.assertContains(response,
        #     '<title>首页 - 网络组内部业务系统</title>',
        #     status_code=200)
        self.assertRedirects(response, '/',status_code=302, target_status_code=200)

        # 错误的登录 没有输入东西
        response = c.post('/accounts/login/', {'username': '', 'password': ''})
        self.assertTemplateUsed('/registration/login.html')
        self.assertContains(response, '用户名这个字段是必填项')
        self.assertContains(response, '密码这个字段是必填项')

        # 错误的登录 用户名密码错误
        response = c.post('/accounts/login/', {'username': 'vincent', 'password': 'asdasdasd'})
        self.assertTemplateUsed('/registration/login.html')
        self.assertContains(response, '请输入正确的用户名和密码。请注意两者都是大小写敏感的。')

# 登录错误之后的错误信息测试,以客户端的方式(selenium)测试
class loginBDDTestCase(LiveServerTestCase):
    fixtures = ['initial_data.json']
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(loginBDDTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(loginBDDTestCase, cls).tearDownClass()

    def test_login(self):
        """
        测试登录错误的时候的提示信息
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        password_input.send_keys(Keys.RETURN)
        # self.selenium.find_element_by_tag_name('button').click()
        
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('请输入正确的用户名和密码。请注意两者都是大小写敏感的。', body.text)
        self.assertIn(unicode('请输入正确的用户名和密码。请注意两者都是大小写敏感的。', "utf-8"), body.text)

        """
        测试 正确登录之后的跳转 是否带参数 返回原来页面  用的是首页
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/?akjasd=ajshdkajshd'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('vincent')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('1q2w3e4r')
        password_input.send_keys(Keys.RETURN)
        # self.selenium.find_element_by_tag_name('button').click()
        current_url = self.selenium.current_url
        current_url_ex = '%s%s' % (self.live_server_url, '/?akjasd=ajshdkajshd')
        self.assertEqual(current_url_ex, current_url)

        # TODO: 测试其它页面登录之后的跳转



