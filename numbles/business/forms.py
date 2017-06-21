from django import forms

from numbles.business.models import Client, Invoice


class EditClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'contact', 'email', 'address')


class EditInvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ('id', 'client', 'date')
