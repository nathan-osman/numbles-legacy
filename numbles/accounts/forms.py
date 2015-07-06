from django import forms

from numbles.accounts.models import Profile


class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="First name [optional].",
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Last name [optional].",
    )
    email = forms.EmailField(
        help_text="Used for displaying Gravatar and password resets.",
    )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'timezone',)
