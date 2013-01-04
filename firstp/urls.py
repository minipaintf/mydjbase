from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from apps.todos.models import Todo
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

class TodoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date Created at',	{'fields': ['created_date']}),
        ('Date updated at',	{'fields': ['updated_date']}),
    ]
    list_display = ('created_date', 'updated_date')

admin.site.register(Todo,TodoAdmin)
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'firstp.views.home', name='home'),
    url(r'^sign_up/$', 'apps.registration.views.sign_up'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    # url(r'^firstp/', include('firstp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^todos/$', 'apps.todos.views.index'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()