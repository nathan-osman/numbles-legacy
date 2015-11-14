from django.conf.urls import patterns, url

urlpatterns = patterns('numbles.ledger.views',

    url(r'^accounts/new/$', 'edit_account', name='new_account'),
    url(r'^accounts/(?P<id>\d+)/$', 'view_account', name='view_account'),
    url(r'^accounts/(?P<id>\d+)/edit/$', 'edit_account', name='edit_account'),
    url(r'^accounts/(?P<id>\d+)/delete/$', 'delete_account', name='delete_account'),

    url(r'^attachments/(?P<id>\d+)/delete/$', 'delete_attachment', name='delete_attachment'),

    url(r'^transactions/new/$', 'edit_transaction', name='new_transaction'),
    url(r'^transactions/find/$', 'find_transaction', name='find_transaction'),
    url(r'^transactions/transfer$', 'transfer', name='transfer'),
    url(r'^transactions/(?P<id>\d+)/$', 'view_transaction', name='view_transaction'),
    url(r'^transactions/(?P<id>\d+)/edit/$', 'edit_transaction', name='edit_transaction'),
    # url(r'^transactions/(?P<id>\d+)/link/$', 'link', name='link'),
    url(r'^transactions/(?P<id>\d+)/unlink/$', 'unlink', name='unlink'),
    url(r'^transactions/(?P<id>\d+)/attach/$', 'attach', name='attach'),
    url(r'^transactions/(?P<id>\d+)/delete/$', 'delete_transaction', name='delete_transaction'),

    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', 'view_month', name='view_month'),
)
