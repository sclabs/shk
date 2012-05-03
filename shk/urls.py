from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # contracts app
    url(r'^contracts/', include('shk.contracts.urls')),

    # auth-related URLs
    #url(r'^login/', shk.views.login),
    #url(r'^logout/', shk.views.logout),

    # admin docs
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
