from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.utils import to_current_timezone
from django.test import RequestFactory, TestCase
from django.utils.timezone import now

from numbles.ledger.models import Account, Transaction
from numbles.ledger.views import transfer


class DummyData:
    """
    Factory for generating dummy instances of classes for testing.
    """

    # Constant value
    VALUE = Decimal('12.99')

    # Use a counter to ensure unique usernames
    _last_user_id = 0

    @classmethod
    def create_user(cls, **kwargs):
        cls._last_user_id += 1
        return User.objects.create_user(
            username='test{}'.format(cls._last_user_id),
            email='test@test.com',
            password='test',
        )

    @classmethod
    def create_account(cls, user, **kwargs):
        kwargs.setdefault('name', 'test')
        return Account.objects.create(
            user=user,
            **kwargs
        )

    @classmethod
    def create_transaction(cls, user, account, **kwargs):
        kwargs.setdefault('date', now())
        kwargs.setdefault('summary', 'test')
        kwargs.setdefault('amount', cls.VALUE)
        return Transaction.objects.create(
            user=user,
            account=account,
            **kwargs
        )

    @classmethod
    def create_chain(cls):
        u = DummyData.create_user()
        a = DummyData.create_account(u)
        t = DummyData.create_transaction(u, a)
        return u, a, t


class TestAccountUpdate(TestCase):

    def test_new(self):
        u, a, t = DummyData.create_chain()
        self.assertEqual(a.balance, t.amount)

    def test_edit(self):
        u, a, t = DummyData.create_chain()
        t.amount = Decimal('0.00')
        t.save()
        self.assertEqual(a.balance, t.amount)

    def test_delete(self):
        u, a, t = DummyData.create_chain()
        t.delete()
        self.assertEqual(a.balance, Decimal('0.00'))

    def test_change(self):
        u, a, t = DummyData.create_chain()
        a2 = DummyData.create_account(u)
        t.account = a2
        t.save()
        self.assertEqual(a.balance, Decimal('0.00'))
        self.assertEqual(a2.balance, t.amount)


class TestViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_transfer(self):
        u, a, t = DummyData.create_chain()
        a2 = DummyData.create_account(u)
        request = self.factory.post(reverse('ledger:transfer'), {
            'from_account': a.id,
            'to_account': a2.id,
            'date': to_current_timezone(now()),
            'amount': DummyData.VALUE,
        })
        request.user = u
        response = transfer(request)
        self.assertEqual(response.status_code, 302)
        a.refresh_from_db()
        a2.refresh_from_db()
        self.assertEqual(a.balance, Decimal('0.00'))
        self.assertEqual(a2.balance, DummyData.VALUE)
