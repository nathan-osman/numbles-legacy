from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from numbles.ledger.forms import AddAccountForm, AddTransactionForm
from numbles.ledger.models import Account, Transaction


@login_required
def add_account(request):
    if request.method == 'POST':
        form = AddAccountForm(data=request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect(account)
    else:
        form = AddAccountForm()
    return render(request, 'form.html', {
        'title': 'Add Account',
        'form': form,
        'description': "Fill in the form below to create a new account.",
    })


@login_required
def view_account(request, id):
    account = get_object_or_404(Account, pk=id, user=request.user)
    return render(request, 'ledger/view_account.html', {
        'title': account,
        'account': account,
    })


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = AddTransactionForm(request.user, data=request.POST)
        if form.is_valid():
            return redirect(form.save())
    else:
        form = AddTransactionForm(request.user, initial={
            'date': now(),
        })
    return render(request, 'form.html', {
        'title': 'Add Transaction',
        'form': form,
        'description': "Fill in the form below to create a new transaction.",
    })


@login_required
def view_transaction(request, id):
    transaction = get_object_or_404(Transaction, pk=id, account__user=request.user)
    return render(request, 'ledger/view_transaction.html', {
        'title': transaction,
        'transaction': transaction,
    })
