# -*- coding: utf-8 -*-
"""
2012-12-23 
"""

from django.test import TestCase
from django.test.client import Client



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





