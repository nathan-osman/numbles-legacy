from django.contrib import admin

from numbles.business.models import Client, Entry, Invoice


admin.site.register(Client)
admin.site.register(Entry)
admin.site.register(Invoice)
