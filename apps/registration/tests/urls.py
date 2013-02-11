# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from apps.registration.views import activate
from apps.registration.views import register


urlpatterns = patterns('',
                       # Test the 'activate' view with custom template
                       # name.
                       url(r'^activate-with-template-name/(?P<activation_key>\w+)/$',
                           activate,
                           {'template_name': 'registration/test_template_name.html'},
                           name='registration_test_activate_template_name'),
                       # Test the 'activate' view with
                       # extra_context_argument.
                       url(r'^activate-extra-context/(?P<activation_key>\w+)/$',
                           activate,
                           {'extra_context': {'foo': 'bar', 'callable': lambda: 'called'}},
                           name='registration_test_activate_extra_context'),
                       # Test the 'activate' view with success_url argument.
                       url(r'^activate-with-success-url/(?P<activation_key>\w+)/$',
                           activate,
                           {'success_url': 'registration_test_custom_success_url'},
                           name='registration_test_activate_success_url'),
                       # Test the 'register' view with custom template
                       # name.
                       url(r'^register-with-template-name/$',
                           register,
                           {'template_name': 'registration/test_template_name.html'},
                           name='registration_test_register_template_name'),
                       # Test the'register' view with extra_context
                       # argument.
                       url(r'^register-extra-context/$',
                           register,
                           {'extra_context': {'foo': 'bar', 'callable': lambda: 'called'}},
                           name='registration_test_register_extra_context'),
                       # Test the 'register' view with custom URL for
                       # closed registration.
                       url(r'^register-with-disallowed-url/$',
                           register,
                           {'disallowed_url': 'registration_test_custom_disallowed'},
                           name='registration_test_register_disallowed_url'),
                       # Set up a pattern which will correspond to the
                       # custom 'disallowed_url' above.
                       url(r'^custom-disallowed/$',
                           direct_to_template,
                           {'template': 'registration/registration_closed.html'},
                           name='registration_test_custom_disallowed'),
                       # Test the 'register' view with custom redirect
                       # on successful registration.
                       url(r'^register-with-success_url/$',
                           register,
                           {'success_url': 'registration_test_custom_success_url'},
                           name='registration_test_register_success_url'
                           ),
                       # Pattern for custom redirect set above.
                       url(r'^custom-success/$',
                           direct_to_template,
                           {'template': 'registration/test_template_name.html'},
                           name='registration_test_custom_success_url'),
                       (r'', include('firstp.urls')),
                       )
