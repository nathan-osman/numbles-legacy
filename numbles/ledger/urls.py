from django.conf.urls import patterns, url

urlpatterns = patterns('numbles.ledger.views',

    url(r'^accounts/add/$', 'edit_account', name='add_account'),
    url(r'^accounts/(?P<id>\d+)/$', 'view_account', name='view_account'),
    url(r'^accounts/(?P<id>\d+)/edit/$', 'edit_account', name='edit_account'),
    url(r'^accounts/(?P<id>\d+)/delete/$', 'delete_account', name='delete_account'),

    url(r'^transactions/add/$', 'edit_transaction', name='add_transaction'),
    url(r'^transactions/transfer/$', 'transfer', name='transfer'),
    url(r'^transactions/(?P<id>\d+)/$', 'view_transaction', name='view_transaction'),
    url(r'^transactions/(?P<id>\d+)/edit/$', 'edit_transaction', name='edit_transaction'),
    url(r'^transactions/(?P<id>\d+)/delete/$', 'delete_transaction', name='delete_transaction'),

    url(r'^(?P<year>\d+)/$', 'view_year', name='view_year'),

    url(r'^search/$', 'search', name='search'),
)
