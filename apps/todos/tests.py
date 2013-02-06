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