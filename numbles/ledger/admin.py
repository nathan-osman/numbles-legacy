from django.contrib import admin

from numbles.ledger.models import Account, Attachment, Tag, Transaction


class AccountAdmin(admin.ModelAdmin):

    def recalculate_balance(self, request, queryset):
        """
        For each account, recalculate its balance.
        """
        for account in queryset:
            account.balance = account.transactions.all().sum()
            account.save()

    actions = (recalculate_balance,)
    list_display = ('name', 'user', 'balance', 'active', 'include_in_balance')
    list_filter = ('user', 'active', 'include_in_balance')
    search_fields = ('name',)


admin.site.register(Account, AccountAdmin)
admin.site.register(Attachment)
admin.site.register(Tag)
admin.site.register(Transaction)
