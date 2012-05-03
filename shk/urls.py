from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # contracts app
    url(r'^contracts/', include('contracts.urls')),

    # auth-related URLs
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/loggedout/'}),
    url(r'^loggedout/', 'shk.views.loggedout'),
    # admin docs
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
