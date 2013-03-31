# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.ucenter.views',
   url(r'^uc.php$', 
    'uc_php',
    name='api_uc_php'),
)