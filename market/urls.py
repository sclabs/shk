from django.conf.urls.defaults import *

urlpatterns = patterns('market.views',
    url(r'^exchange/$', 'exchange'),
    url(r'^ious/$', 'ious', name='ious'),
    url(r'^ious/recall/(\d+)/$', 'recall', name='recall'),
    url(r'^contracts/$', 'contracts', name='contracts'),
    url(r'^contracts/complete/(\d+)/$', 'complete', name='complete'),
    url(r'^contracts/fail/(\d+)/$', 'fail', name='fail'),
    url(r'^villages/$', 'villages', name='villages'),
    url(r'^villages/add/$', 'addVillage', name='addVillage'),
    url(r'^villages/remove/(\d+)/$', 'removeVillage', name='removeVillage'),
)
