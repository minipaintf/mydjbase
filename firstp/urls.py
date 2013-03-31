# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'firstp.views.home', name='home'),
    #url(r'^sign_up/$', 'apps.registration.views.sign_up'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/', include('apps.registration.urls')),
    # ucenter
    (r'^api/', include('apps.ucenter.urls')),
    # url(r'^firstp/', include('firstp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()