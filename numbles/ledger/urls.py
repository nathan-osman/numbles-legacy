from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^accounts/new/$', views.edit_account, name='new_account'),
    url(r'^accounts/(?P<id>\d+)/$', views.view_account, name='view_account'),
    url(r'^accounts/(?P<id>\d+)/edit/$', views.edit_account, name='edit_account'),
    url(r'^accounts/(?P<id>\d+)/delete/$', views.delete_account, name='delete_account'),
    url(r'^accounts/(?P<id>\d+)/transactions/$', views.view_transactions, name='view_transactions'),

    url(r'^attachments/(?P<id>\d+)/delete/$', views.delete_attachment, name='delete_attachment'),

    url(r'^tags/new/$', views.edit_tag, name='new_tag'),
    url(r'^tags/(?P<id>\d+)/edit/$', views.edit_tag, name='edit_tag'),
    url(r'^tags/(?P<id>\d+)/delete/$', views.delete_tag, name='delete_tag'),

    url(r'^transactions/$', views.transactions, name='transactions'),
    url(r'^transactions/new/$', views.edit_transaction, name='new_transaction'),
    url(r'^transactions/transfer$', views.transfer, name='transfer'),
    url(r'^transactions/(?P<id>\d+)/$', views.view_transaction, name='view_transaction'),
    url(r'^transactions/(?P<id>\d+)/edit/$', views.edit_transaction, name='edit_transaction'),
    url(r'^transactions/(?P<id>\d+)/link/$', views.link, name="link"),
    url(r'^transactions/(?P<id>\d+)/unlink/(?P<id2>\d+)/$', views.unlink, name='unlink'),
    url(r'^transactions/(?P<id>\d+)/attach/$', views.attach, name='attach'),
    url(r'^transactions/(?P<id>\d+)/delete/$', views.delete_transaction, name='delete_transaction'),

    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', views.view_month, name='view_month'),
]
