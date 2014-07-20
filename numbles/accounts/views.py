from django.shortcuts import redirect, render

from numbles.accounts.forms import EditProfileForm


def profile(request):
    if request.method == 'POST':
        form = EditProfileForm(instance=request.user.profile, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user.profile)
    return render(request, 'form.html', {
        'title': 'Edit Profile',
        'form': form,
    })
