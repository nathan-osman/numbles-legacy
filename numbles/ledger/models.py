from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


class Account(models.Model):

    user = models.ForeignKey(User)

    name = models.CharField(max_length=40,
                            help_text="Account name.")
    include_in_balance = models.BooleanField(default=False)

    balance = models.DecimalField(max_digits=9,
                                  decimal_places=2,
                                  default=0)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('ledger:view_account', (), {
            'id': self.id,
        })


class Transaction(models.Model):

    account = models.ForeignKey(Account, related_name='transactions')

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

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return self.summary

    @models.permalink
    def get_absolute_url(self):
        return ('ledger:view_transaction', (), {
            'id': self.id,
        })


@receiver(models.signals.post_init, sender=Transaction)
def store_original_amount(instance, **kwargs):
    """
    Store the original amount of the transaction.
    This is necessary so that the difference can be calculated when the
    transaction is modified or deleted.
    """
    instance.original_amount = instance.amount or 0


@receiver(models.signals.post_save, sender=Transaction)
def update_account_balance_post_save(instance, **kwargs):
    """
    Update the transaction's account balance.
    The account stores the sum of all transactions. By calculating the
    difference of the transaction from its previous value, the sum will
    continue to reflect the correct sum.
    """
    instance.account.balance = models.F('balance') + (instance.amount - instance.original_amount)
    instance.account.save()


@receiver(models.signals.post_delete, sender=Transaction)
def update_account_balance_post_delete(instance, **kwargs):
    """
    Remove the transaction amount from the account balance.
    """
    instance.account.balance = models.F('balance') - instance.amount
    instance.account.save()
