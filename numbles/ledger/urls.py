from django.conf.urls import patterns, url

urlpatterns = patterns('numbles.ledger.views',

    url(r'^account/add/$', 'edit_account', name='add_account'),
    url(r'^account/(?P<id>\d+)/$', 'view_account', name='view_account'),
    url(r'^account/(?P<id>\d+)/edit/$', 'edit_account', name='edit_account'),
    url(r'^account/(?P<id>\d+)/delete/$', 'delete_account', name='delete_account'),

    url(r'^transaction/add/$', 'edit_transaction', name='add_transaction'),
    url(r'^transaction/transfer/$', 'transfer', name='transfer'),
    url(r'^transaction/(?P<id>\d+)/$', 'view_transaction', name='view_transaction'),
    url(r'^transaction/(?P<id>\d+)/edit/$', 'edit_transaction', name='edit_transaction'),
    url(r'^transaction/(?P<id>\d+)/delete/$', 'delete_transaction', name='delete_transaction'),
)
