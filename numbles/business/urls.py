from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^clients/$', views.view_clients, name='view_clients'),
    url(r'^clients/new/$', views.edit_client, name='new_client'),
    url(r'^clients/(?P<id>\d+)/$', views.view_client, name='view_client'),
    url(r'^clients/(?P<id>\d+)/edit/$', views.edit_client, name='edit_client'),
    url(r'^clients/(?P<id>\d+)/delete/$', views.delete_client, name='delete_client'),

    url(r'^invoices/$', views.view_invoices, name='view_invoices'),
    url(r'^invoices/new/$', views.edit_invoice, name='new_invoice'),
    url(r'^invoices/(?P<id>\d+)/$', views.view_invoice, name='view_invoice'),
    url(r'^invoices/(?P<id>\d+)/edit/$', views.edit_invoice, name="edit_invoice"),
    url(r'^invoices/(?P<id>\d+)/delete/$', views.delete_invoice, name="delete_invoice"),
]
