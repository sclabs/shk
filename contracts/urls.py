from django.conf.urls.defaults import *

urlpatterns = patterns('contracts.views',
    url(r'^exchange/$', 'exchange'),
    url(r'^ious/$', 'ious', name='ious'),
    url(r'^contracts/$', 'contracts', name='contracts'),
    url(r'^recall/(\d+)/$', 'recall', name='recall'),
    url(r'^villages/$', 'villages', name='villages'),
    url(r'^villages/add/$', 'addVillage', name='addVillage'),
    url(r'^villages/remove/(\d+)/$', 'removeVillage', name='removeVillage'),
)
