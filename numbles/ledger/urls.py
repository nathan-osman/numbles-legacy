from django.conf.urls import patterns, url

urlpatterns = patterns('numbles.ledger.views',

    url(r'^account/new/$', 'new_account', name='new_account'),
    url(r'^account/(?P<id>\d+)/$', 'view_account', name='view_account'),
)
