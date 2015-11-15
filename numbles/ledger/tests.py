from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from numbles.ledger.models import Account, Transaction


class TestAccountUpdate(TestCase):

    def create_transaction_chain(self):
        u = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='test',
        )
        a = Account.objects.create(
            user=u,
            name='Test',
        )
        t = Transaction()
        t.user = u
        t.account = a
        t.date = now()
        t.summary = 'Test'
        t.amount = Decimal('12.99')
        t.save()
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

    def test_change(self):
        u, a1, t = self.create_transaction_chain()
        a2 = Account.objects.create(
            user=u,
            name='Test2',
        )
        t.account = a2
        t.save()
        self.assertEqual(a1.balance, Decimal('0.00'))
        self.assertEqual(a2.balance, t.amount)
