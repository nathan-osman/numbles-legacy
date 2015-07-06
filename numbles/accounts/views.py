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
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(
            instance=request.user.profile,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            },
        )
    return render(request, 'pages/form.html', {
        'title': 'Edit Profile',
        'form': form,
    })
