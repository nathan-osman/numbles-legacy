from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from pytz import timezone

from numbles.ledger.models import Account, Year, Transaction


class UtilMixin:

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'test')

    def create_account(self, **kwargs):
        kwargs.setdefault('user', self.user)
        kwargs.setdefault('total', self.user.total)
        kwargs.setdefault('balance', Decimal('12.99'))
        kwargs.setdefault('name', 'Test')
        kwargs.setdefault('include_in_balance', True)
        return Account.objects.create(**kwargs)

    def create_transaction(self, **kwargs):
        kwargs.setdefault('user', self.user)
        kwargs.setdefault('date', datetime(2000, 1, 1, tzinfo=timezone('UTC')))
        kwargs.setdefault('summary', 'Test')
        kwargs.setdefault('amount', Decimal('12.99'))
        return Transaction.objects.create(**kwargs)

    def check_balances(self, id, amount, account_balance=None, total_balance=None):
        transaction = Transaction.objects.get(pk=id)
        self.assertEqual(transaction.year.balance, amount)
        self.assertEqual(transaction.account.balance, account_balance or amount)
        self.assertEqual(transaction.account.total.balance, total_balance or amount)


class TestTotalUpdate(UtilMixin, TestCase):

    def test_total_update(self):
        self.create_account()
        self.user.total.update()
        self.assertEqual(self.user.total.balance, Decimal('12.99'))
        self.create_account(balance=Decimal('1.01'))
        self.user.total.update()
        self.assertEqual(self.user.total.balance, Decimal('14.00'))


class TestYearDeleted(UtilMixin, TestCase):

    def test_year_deleted(self):
        transaction = self.create_transaction(account=self.create_account())
        transaction.delete()
        self.assertEqual(Year.objects.count(), 0)


class TestIncludeBalance(UtilMixin, TestCase):

    def test_include_balance(self):
        self.create_account()
        self.create_account(include_in_balance=False)
        self.user.total.update()
        self.assertEqual(self.user.total.balance, Decimal('12.99'))


class TestTransactionSave(UtilMixin, TestCase):

    def test_transaction_save(self):
        transaction = self.create_transaction(account=self.create_account())
        self.check_balances(transaction.id, Decimal('12.99'))
        transaction.amount = Decimal('3.99')
        transaction.save()
        self.check_balances(transaction.id, Decimal('3.99'))
        transaction.name = "Renamed Test"
        transaction.save()
        self.check_balances(transaction.id, Decimal('3.99'))


class TestTransactionChangeYear(UtilMixin, TestCase):

    def test_transaction_change_year(self):
        transaction = self.create_transaction(account=self.create_account())
        transaction.date = datetime(2001, 1, 1, tzinfo=timezone('UTC'))
        transaction.save()
        self.assertEqual(Year.objects.count(), 1)
        self.assertEqual(Year.objects.first().year, 2001)
        self.check_balances(transaction.id, Decimal('12.99'))


class TestTransactionChangeAccount(UtilMixin, TestCase):

    def test_transaction_change_account(self):
        account = self.create_account()
        self.create_transaction(account=account, amount=Decimal('1.01'))
        transaction = self.create_transaction(account=account)
        transaction.account = self.create_account()
        transaction.save()
        self.assertEqual(Year.objects.count(), 2)
        self.check_balances(transaction.id, Decimal('12.99'), total_balance=Decimal('14.00'))
