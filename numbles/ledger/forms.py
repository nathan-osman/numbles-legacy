from django import forms

from numbles.ledger.models import Account, Transaction


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('name', 'include_in_balance')


class DeleteAccountForm(forms.Form):

    confirm = forms.BooleanField(label="I confirm that I wish to delete this account (cannot be undone).")


class EditTransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('account', 'date', 'summary', 'description', 'amount', 'reconciled')

    def __init__(self, user, *args, **kwargs):
        super(EditTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)


class TransferBetweenAccountsForm(forms.Form):

    from_account = forms.ModelChoiceField(None)
    to_account = forms.ModelChoiceField(None)

    date = forms.DateTimeField()
    amount = forms.DecimalField(max_digits=9,
                                decimal_places=2,
                                help_text="Amount to transfer.")

    def __init__(self, user, *args, **kwargs):
        super(TransferBetweenAccountsForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(user=user)
        self.fields['to_account'].queryset = Account.objects.filter(user=user)

    def clean(self):
        cleaned_data = super(TransferBetweenAccountsForm, self).clean()
        if cleaned_data['from_account'] == cleaned_data['to_account']:
            raise forms.ValidationError("You must select two different accounts.")
        return cleaned_data


class DeleteTransactionForm(forms.Form):

    confirm = forms.BooleanField(label="I confirm that I wish to delete this transaction (cannot be undone).")
