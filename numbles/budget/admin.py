from django.contrib import admin

from numbles.budget.models import Category, Item


class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('next',)


admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
