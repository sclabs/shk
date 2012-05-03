from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # contracts app
    url(r'^contracts/', include('contracts.urls')),

    # auth-related URLs
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/loggedout/'}),
    url(r'^switchuser/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^loggedout/$', 'shk.views.loggedout'),
    url(r'^changepassword/$', 'django.contrib.auth.views.password_change'),
    url(r'^passwordchanged/$', 'django.contrib.auth.views.password_change_done'),

    # admin docs
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
