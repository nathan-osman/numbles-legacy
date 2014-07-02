from django.conf.urls import patterns, url

urlpatterns = patterns('numbles.ledger.views',

    url(r'^account/add/$', 'add_account', name='add_account'),
    url(r'^account/(?P<id>\d+)/$', 'view_account', name='view_account'),

    url(r'^transaction/add/$', 'add_transaction', name='add_transaction'),
    url(r'^transaction/(?P<id>\d+)/$', 'view_transaction', name='view_transaction'),
)
