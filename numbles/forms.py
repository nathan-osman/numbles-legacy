from django import forms


class DeleteForm(forms.Form):

    confirm = forms.BooleanField(label="I confirm that I wish to do this (cannot be undone).")
