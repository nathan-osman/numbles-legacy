from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from numbles.accounts.forms import EditProfileForm


@login_required
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        form = EditProfileForm(instance=request.user.profile, data=request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(
            instance=request.user.profile,
            initial={
                'email': request.user.email,
            },
        )
    return render(request, 'form.html', {
        'title': 'Edit Profile',
        'form': form,
    })
