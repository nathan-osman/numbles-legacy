from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^invoices/$', views.view_invoices, name='view_invoices'),
]
