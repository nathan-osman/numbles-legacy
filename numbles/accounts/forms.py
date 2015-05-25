from django import forms

from numbles.accounts.models import Profile


class EditProfileForm(forms.ModelForm):

    email = forms.EmailField(
        help_text="Used for displaying Gravatar.",
    )

    class Meta:
        model = Profile
        fields = ('email', 'timezone',)
