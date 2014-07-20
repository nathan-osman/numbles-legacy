from django import forms

from numbles.accounts.models import Profile


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('timezone',)
