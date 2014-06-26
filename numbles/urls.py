from django.conf.urls import include, patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'numbles.views.index', name='home'),

    url(r'^admin/', include(admin.site.urls)),
)
