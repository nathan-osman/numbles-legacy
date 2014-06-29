from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from numbles.ledger.forms import NewAccountForm
from numbles.ledger.models import Account


@login_required
def new_account(request):
    if request.method == 'POST':
        form = NewAccountForm(data=request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect(account)
    else:
        form = NewAccountForm()
    return render(request, 'form.html', {
        'title': 'New Account',
        'form': form,
        'description': "Fill in the form below to create a new account.",
    })


@login_required
def view_account(request, id):
    account = get_object_or_404(Account, pk=id)
    return render(request, 'ledger/view_account.html', {
        'title': account.name,
        'account': account,
    })
