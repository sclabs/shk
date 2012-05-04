from django.conf.urls.defaults import *

urlpatterns = patterns('contracts.views',
    url(r'^exchange/$', 'exchange'),
    url(r'^ious/$', 'IOUs'),
    url(r'^contracts/$', 'contracts'),
    url(r'^villages/$', 'villages', name='villages'),
    url(r'^villages/add/$', 'addVillage', name='addVillage'),
    url(r'^villages/remove/(\d+)/$', 'removeVillage', name='removeVillage'),
)
