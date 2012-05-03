from django.conf.urls.defaults import *

urlpatterns = patterns('contracts.views',
    url(r'^exchange/$', 'exchange'),
    url(r'^ious/$', 'IOUs'),
    url(r'^contracts/$', 'contracts'),
)
