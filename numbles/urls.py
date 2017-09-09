from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/', include('numbles.accounts.urls', 'accounts')),
    url(r'^business/', include('numbles.business.urls', 'business')),
    url(r'^ledger/', include('numbles.ledger.urls', 'ledger')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
