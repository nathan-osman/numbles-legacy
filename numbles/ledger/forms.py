from django import forms

from numbles.ledger.models import Account, Attachment, Tag, Transaction


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('name', 'active', 'include_in_balance')


class DeleteForm(forms.Form):

    confirm = forms.BooleanField(label="I confirm that I wish to delete this object (cannot be undone).")


class EditTagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name', 'color')


class EditTransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('account', 'date', 'summary', 'description', 'amount', 'reconciled', 'tags')

    def __init__(self, user, *args, **kwargs):
        super(EditTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = user.accounts.all()


class FindTransactionForm(forms.Form):
    """
    Search form displayed in the sidebar and on the search page.
    """
    query = forms.CharField(required=False)
    account = forms.ModelChoiceField(None, required=False, empty_label="(All)")
    tag = forms.ModelChoiceField(None, required=False, empty_label="(All)")

    def __init__(self, user, *args, **kwargs):
        super(FindTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = user.accounts.all()
        self.fields['tag'].queryset = user.tags.all()


class TransferForm(forms.Form):

    from_account = forms.ModelChoiceField(None)
    to_account = forms.ModelChoiceField(None)

    date = forms.DateTimeField()
    amount = forms.DecimalField(
        max_digits=9,
        decimal_places=2,
        help_text="Amount to transfer.",
    )

    def __init__(self, user, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].queryset = user.accounts.all()
        self.fields['to_account'].queryset = user.accounts.all()

    def clean(self):
        cleaned_data = super(TransferForm, self).clean()
        if 'from_account' in cleaned_data and 'to_account' in cleaned_data and \
                cleaned_data['from_account'] == cleaned_data['to_account']:
            raise forms.ValidationError("You must select two different accounts.")
        return cleaned_data


class AttachForm(forms.ModelForm):

    class Meta:
        model = Attachment
        fields = ('summary', 'file')
