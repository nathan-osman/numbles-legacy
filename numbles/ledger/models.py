from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


# TODO: this should be a configurable setting
MAX_DIGITS = 9
DECIMAL_PLACES = 2


def disable_for_fixture(fn):
    """
    Disable signal handler if fixture is being loaded.
    """
    def wrap(*args, **kwargs):
        if not kwargs['raw']:
            return fn(*args, **kwargs)
    return wrap


class UpdateMixin(object):

    def update(self, update_parent=True):
        """
        Update the field with the sum of a related field.

        UPDATE_QUERYSET must be set to the queryset that includes all rows to be
        summed. UPDATE_FIELD is the name of the related field to be summed. If
        UPDATE_PARENT is set, then it too will recalculate the sum.
        """
        data = self.UPDATE_QUERYSET().aggregate(sum=models.Sum(self.UPDATE_FIELD))
        setattr(self, 'balance', data['sum'] or Decimal('0.00'))
        self.save()
        if self.UPDATE_PARENT and update_parent:
            getattr(self, self.UPDATE_PARENT).update()


class Total(models.Model, UpdateMixin):
    """
    The total balance for specific accounts chosen by the user.

    The purpose of this class is to store the total balance of all accounts
    where Account.include_in_balance is set to True.
    """

    UPDATE_QUERYSET = lambda self: self.accounts.filter(include_in_balance=True)
    UPDATE_FIELD = 'balance'
    UPDATE_PARENT = None

    user = models.OneToOneField(
        User,
        primary_key=True,
    )

    balance = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=Decimal('0.00'),
    )

    def __unicode__(self):
        return unicode(self.balance)


@receiver(models.signals.post_save, sender=User)
@disable_for_fixture
def on_user_save(instance, created, **kwargs):
    """
    Create a Total instance whenever a user is created.
    """
    if created:
        Total.objects.create(user=instance)


class Account(models.Model, UpdateMixin):
    """
    A distinct set of transactions.
    """

    UPDATE_QUERYSET = lambda self: self.years.all()
    UPDATE_FIELD = 'balance'
    UPDATE_PARENT = 'total'

    user = models.ForeignKey(
        User,
        related_name='accounts',
    )

    total = models.ForeignKey(
        Total,
        related_name='accounts',
    )

    balance = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=Decimal('0.00'),
    )

    name = models.CharField(
        max_length=40,
        help_text="Account name.",
    )

    active = models.BooleanField(default=True)
    include_in_balance = models.BooleanField(default=False)

    class Meta:
        ordering = ('-balance', 'name')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('ledger:view_account', (), {'id': self.id})


@receiver(models.signals.post_delete, sender=Account)
def on_account_delete(instance, **kwargs):
    """
    Remove the account's balance from the total balance.
    """
    if instance.include_in_balance:
        instance.total.update()


class Year(models.Model, UpdateMixin):
    """
    Transactions for a given year.
    """

    UPDATE_QUERYSET = lambda self: self.transactions.all()
    UPDATE_FIELD = 'amount'
    UPDATE_PARENT = 'account'

    user = models.ForeignKey(
        User,
        related_name='years',
    )

    account = models.ForeignKey(
        Account,
        related_name='years',
    )

    balance = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=Decimal('0.00'),
    )

    year = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('year',)

    def __unicode__(self):
        return unicode(self.year)

    def update(self, *args, **kwargs):
        """
        Self destruct if no longer needed.
        """
        if not self.transactions.count():
            self.delete()
        else:
            super(Year, self).update(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Year)
def on_year_delete(instance, **kwargs):
    """
    Remove the year's balance from the account balance.
    """
    instance.account.update()


class Transaction(models.Model):
    """
    An amount transferred from or to an account.
    """

    user = models.ForeignKey(
        User,
        related_name='transactions',
    )

    account = models.ForeignKey(
        Account,
        related_name='transactions',
    )

    year = models.ForeignKey(
        Year,
        related_name='transactions',
    )

    date = models.DateTimeField(help_text="Date and time of the transaction.")

    summary = models.CharField(
        max_length=100,
        help_text="Brief description of the transaction.",
    )

    description = models.TextField(
        blank=True,
        help_text="Additional details or information.",
    )

    amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        help_text="Amount of the transaction.",
    )

    reconciled = models.BooleanField(default=False)

    # This is used by transactions between accounts
    linked = models.ForeignKey(
        'self',
        null=True,
        blank=True,
    )

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
def on_transaction_init(instance, **kwargs):
    """
    Store the original year and amount of the transaction.
    """
    instance.original_account = instance.account if hasattr(instance, 'account') else None
    instance.original_year = instance.year if hasattr(instance, 'year') else None
    instance.original_amount = instance.amount


@receiver(models.signals.pre_save, sender=Transaction)
@disable_for_fixture
def on_transaction_pre_save(instance, **kwargs):
    """
    Set the appropriate Year for the transaction.
    """
    instance.year, _ = Year.objects.get_or_create(
        user=instance.user,
        account=instance.account,
        year=instance.date.year,
    )


@receiver(models.signals.post_save, sender=Transaction)
@disable_for_fixture
def on_transaction_post_save(instance, created, **kwargs):
    """
    Update the transaction's year and account balance.

    If the year has changed, check to see if the old year no longer contains any
    transactions. If so, delete it. Also, the new year might not exist, so
    create it if this is the case.
    """
    account_changed = instance.original_account != instance.account
    year_changed = instance.original_year != instance.year
    amount_changed = instance.original_amount != instance.amount
    if created or account_changed or year_changed or amount_changed:
        if not created and (account_changed or year_changed):
            instance.original_year.update(account_changed)
        instance.year.update()
    on_transaction_init(instance)


@receiver(models.signals.post_delete, sender=Transaction)
def on_transaction_delete(instance, **kwargs):
    """
    Remove the transaction's amount from the year's balance.
    """
    instance.year.update()
