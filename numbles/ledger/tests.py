from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from pytz import timezone

from numbles.ledger.models import Account, Transaction


class UtilMixin:
    """
    Provide a set of helper methods for generating "dummy" data.
    """

    def create_user(self, **kwargs):
        self._n = getattr(self, '_n', 0) + 1
        kwargs.setdefault('username', 'test{}'.format(self._n))
        kwargs.setdefault('email', 'test@test.com')
        kwargs.setdefault('password', 'test')
        return User.objects.create_user(**kwargs)

    def create_account(self, user, **kwargs):
        kwargs.setdefault('user', user)
        kwargs.setdefault('name', 'Test')
        return Account.objects.create(**kwargs)

    def create_transaction(self, user, **kwargs):
        kwargs.setdefault('user', user)
        kwargs.setdefault('date', datetime(2000, 1, 1, tzinfo=timezone('UTC')))
        kwargs.setdefault('summary', 'Test')
        kwargs.setdefault('amount', Decimal('12.99'))
        t = Transaction()
        for k, v in kwargs.items():
            setattr(t, k, v)
        t.save()
        return t


class TestAccountUpdate(UtilMixin, TestCase):

    def create_transaction_chain(self):
        u = self.create_user()
        a = self.create_account(u)
        t = self.create_transaction(u, account=a)
        return u, a, t

    def test_new(self):
        u, a, t = self.create_transaction_chain()
        self.assertEqual(a.balance, t.amount)

    def test_edit(self):
        u, a, t = self.create_transaction_chain()
        t.amount = Decimal('0.00')
        t.save()
        self.assertEqual(a.balance, t.amount)

    def test_delete(self):
        u, a, t = self.create_transaction_chain()
        t.delete()
        self.assertEqual(a.balance, Decimal('0.00'))
