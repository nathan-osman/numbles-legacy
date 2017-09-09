from django import forms

from numbles.business.models import Client, Entry, Invoice


class EditClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'contact', 'email', 'address')


class EditEntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ('invoice', 'description', 'amount')

    def __init__(self, user, *args, **kwargs):
        super(EditEntryForm, self).__init__(*args, **kwargs)
        self.fields['invoice'].queryset = user.invoices.all()


class EditInvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ('id', 'client', 'date', 'status')
