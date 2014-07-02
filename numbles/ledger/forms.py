from django import forms

from numbles.ledger.models import Account, Transaction


class AddAccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('name', 'include_in_balance')


class AddTransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('account', 'date', 'summary', 'description', 'amount', 'reconciled')

    def __init__(self, user, *args, **kwargs):
        super(AddTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)
