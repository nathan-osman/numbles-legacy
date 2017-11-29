from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^items/new/$', views.edit_item, name='new_item'),
    url(r'^items/(?P<id>\d+)/edit/$', views.edit_item, name='edit_item'),
]
