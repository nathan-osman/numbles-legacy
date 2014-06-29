from django import forms

from numbles.ledger.models import Account, Transaction


class NewAccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('name', 'include_in_balance')


class NewTransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('date', 'summary', 'description', 'amount', 'reconciled')
