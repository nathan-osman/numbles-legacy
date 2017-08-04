from django import forms
from django.conf import settings

from numbles.ledger.models import Account, Attachment, Tag, Transaction


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('name', 'active', 'include_in_balance')


class EditTagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name', 'color')


class TransactionForm(forms.Form):
    """
    Form for filtering transactions
    """

    date_from = forms.DateTimeField(required=False)
    date_to = forms.DateTimeField(required=False)
    query = forms.CharField(required=False)
    account = forms.ModelChoiceField(None, required=False, empty_label="(All)")
    tag = forms.ModelChoiceField(None, required=False, empty_label="(All)")
    reconciled = forms.NullBooleanField()
    amount_min = forms.DecimalField(
        required=False,
        label="Amount minimum",
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
    )
    amount_max = forms.DecimalField(
        required=False,
        label="Amount maximum",
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
    )
    has_attachment = forms.NullBooleanField()

    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = user.accounts.all()
        self.fields['tag'].queryset = user.tags.all()


class EditTransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('account', 'date', 'summary', 'description', 'amount', 'reconciled', 'tags')

    def __init__(self, user, *args, **kwargs):
        super(EditTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = user.accounts.all()
        self.fields['tags'].queryset = user.tags.all()


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


class LinkForm(forms.Form):

    transaction_id = forms.ModelChoiceField(
        queryset=None,
        label="Transaction ID",
        widget=forms.NumberInput(),
    )

    def __init__(self, user, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields['transaction_id'].queryset = Transaction.objects.all()


class AttachForm(forms.ModelForm):

    class Meta:
        model = Attachment
        fields = ('summary', 'file')
