from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from numbles.ledger.models import Total, Account


class UtilMixin:

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'test')

    def create_account(self, balance):
        return Account.objects.create(
            user=self.user,
            total=self.user.total,
            balance=balance,
            name='Account',
            include_in_balance=True
        )


class TestTotalCreated(UtilMixin, TestCase):

    def test_total_created(self):
        Total.objects.get(pk=self.user.id)


class TestTotalUpdate(UtilMixin, TestCase):

    def test_total_update(self):
        self.create_account(Decimal('12.99'))
        self.user.total.update()
        self.assertEqual(self.user.total.balance, Decimal('12.99'))
