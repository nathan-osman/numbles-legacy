from django import forms

from .models import Item


class EditItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('name', 'description', 'cron', 'amount')
