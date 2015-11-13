from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import make_aware


# TODO: this should be a configurable setting
MAX_DIGITS = 9
DECIMAL_PLACES = 2


class UpdateMixin(object):
    """
    Empty class that exists for legacy purposes.
    (TODO: remove this when old migrations are no longer needed.)
    """


class AccountQuerySet(models.QuerySet):
    """
    Provides custom methods for account queries.
    """

    def sum(self):
        """
        Calculate the sum of account balances in the query set.
        """
        return self.aggregate(sum=models.Sum('balance'))['sum'] or Decimal('0.00')
    sum.queryset_only = True


class Account(models.Model):
    """
    A distinct set of transactions, typically associated with a physical
    location (i.e., bank, cash drawer, etc.).
    """

    user = models.ForeignKey(User, related_name='accounts')
    name = models.CharField(max_length=40, help_text="Account name")

    balance = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=Decimal('0.00'),
    )

    active = models.BooleanField(default=True)
    include_in_balance = models.BooleanField(default=False)

    objects = AccountQuerySet.as_manager()

    class Meta:
        ordering = ('-balance', 'name')

    def __unicode__(self):
        return self.name

    def adjust_balance(self, amount):
        """
        Adjust the balance by the specified amount.
        """
        self.balance += amount
        self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('ledger:view_account', (), {'id': self.id})


class Tag(models.Model):
    """
    Category or "grouping" for transactions.
    """

    COLORS = (
        ('#773333', "Red"),
        ('#337733', "Green"),
        ('#333377', "Blue"),
        ('#777733', "Yellow"),
        ('#773377', "Magenta"),
        ('#337777', "Cyan"),
    )

    user = models.ForeignKey(User, related_name='tags')
    name = models.CharField(max_length=20, help_text="Descriptive name")
    color = models.CharField(max_length=7, choices=COLORS, help_text="Background color")

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class TransactionQuerySet(models.QuerySet):
    """
    Provides custom methods for transaction queries.
    """

    def sum(self):
        """
        Calculate the sum of transactions in the query set.
        """
        return self.aggregate(sum=models.Sum('amount'))['sum'] or Decimal('0.00')
    sum.queryset_only = True


class Transaction(models.Model):
    """
    An amount transferred to or from an account.
    """

    user = models.ForeignKey(User, related_name='transactions')
    account = models.ForeignKey(Account, related_name='transactions')

    date = models.DateTimeField(help_text="Date and time of the transaction")
    summary = models.CharField(max_length=100, help_text="Brief description of the transaction")
    description = models.TextField(blank=True, help_text="Additional details or information")

    amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        help_text="Amount of the transaction",
    )

    reconciled = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='transactions')

    linked = models.ForeignKey('self', null=True, blank=True)

    objects = TransactionQuerySet.as_manager()

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return self.summary

    @classmethod
    def month(cls, year, month, **kwargs):
        """
        Create a queryset for all transactions within the specified month.
        Additional filters can be supplied in order to filter results.
        """
        start = make_aware(datetime(year, month, 1))
        end = make_aware(datetime(year + month / 12, month % 12 + 1, 1))
        return cls.objects.filter(date__gte=start, date__lt=end, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('ledger:view_transaction', (), {'id': self.id})


@receiver(models.signals.post_init, sender=Transaction)
def on_transaction_init(instance, **kwargs):
    """
    Store the initial value of the transaction's account and amount.
    """
    instance.original_account = getattr(instance, 'account', None)
    instance.original_amount = getattr(instance, 'amount', None)


@receiver(models.signals.post_save, sender=Transaction)
def on_transaction_save(instance, created, **kwargs):
    """
    Adjust the balance of the account(s) involved in the transaction.
    """
    if instance.original_account != instance.account:
        if instance.original_account is not None:
            instance.original_account.adjust_balance(-instance.original_amount)
        instance.account.adjust_balance(instance.amount)
    else:
        instance.account.adjust_balance(instance.amount - instance.original_amount)


@receiver(models.signals.post_delete, sender=Transaction)
def on_transaction_delete(instance, **kwargs):
    """
    Remove the transaction balance from the account.
    """
    instance.account.adjust_balance(-instance.amount)
