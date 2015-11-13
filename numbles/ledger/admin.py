from django.contrib import admin

from numbles.ledger.models import Account, Attachment, Tag, Transaction


admin.site.register(Account)
admin.site.register(Attachment)
admin.site.register(Tag)
admin.site.register(Transaction)
