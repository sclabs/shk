from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # contracts app
    url(r'^market/', include('market.urls')),

    # auth-related URLs
    url(r'^login/$', 'django.contrib.auth.views.login',),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/loggedout/'}),
    url(r'^switchuser/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^loggedout/$', 'shk.views.loggedout'),
    url(r'^changepassword/$', 'django.contrib.auth.views.password_change'),
    url(r'^passwordchanged/$', 'django.contrib.auth.views.password_change_done'),

    # password reset urls (not working)
    #url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    #url(r'^resetsent/$', 'django.contrib.auth.views.password_reset_done'),
    #url(r'^setnewpassword/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    #url(r'^setnewpassword/[0-9A-Za-z]+-.+/$', 'django.contrib.auth.views.password_reset_confirm'),
    #url(r'^resetcomplete/$', 'django.contrib.auth.views.password_reset_complete'),

    # admin docs
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
