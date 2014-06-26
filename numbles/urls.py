from django.conf.urls import include, patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'numbles.views.index', name='home'),

    url(r'^accounts/', include('numbles.accounts.urls', 'accounts')),

    url(r'^admin/', include(admin.site.urls)),
)
