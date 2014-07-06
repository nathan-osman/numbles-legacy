from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


class Account(models.Model):

    user = models.ForeignKey(User)

    name = models.CharField(max_length=40,
                            help_text="Account name.")
    include_in_balance = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('ledger:view_account', (), {
            'id': self.id,
        })


class Transaction(models.Model):

    account = models.ForeignKey(Account)

    date = models.DateTimeField(help_text="Date and time of the transaction.")
    summary = models.CharField(max_length=100,
                               help_text="Brief description of the transaction.")
    description = models.TextField(blank=True,
                                   help_text="Additional details or information.")
    amount = models.DecimalField(max_digits=9,
                                 decimal_places=2,
                                 help_text="Amount of the transaction.")
    reconciled = models.BooleanField(default=False)

    # This is used by transactions between accounts
    linked = models.ForeignKey('self',
                               null=True,
                               blank=True)

    def __unicode__(self):
        return self.summary

    @models.permalink
    def get_absolute_url(self):
        return ('ledger:view_transaction', (), {
            'id': self.id,
        })

    @property
    def amount_formatted(self):
        if self.amount > 0:
            return mark_safe('<span class="text-success">$%s</span>' % self.amount)
        elif self.amount == 0:
            return mark_safe('$%s' % self.amount)
        else:
            return mark_safe('<span class="text-danger">-$%s</span>' % abs(self.amount))
