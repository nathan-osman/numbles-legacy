from django.contrib import admin

from numbles.ledger.models import Account, Transaction


admin.site.register(Account)
admin.site.register(Transaction)
