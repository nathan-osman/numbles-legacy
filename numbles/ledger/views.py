from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from numbles.ledger.forms import AddAccountForm, AddTransactionForm, TransferBetweenAccountsForm
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
@transaction.atomic
def transfer(request):
    if request.method == 'POST':
        form = TransferBetweenAccountsForm(request.user, data=request.POST)
        if form.is_valid():
            from_transaction = Transaction(
                account=form.cleaned_data['from_account'],
                date=form.cleaned_data['date'],
                summary="Transfer to %s" % form.cleaned_data['to_account'],
                amount=(-form.cleaned_data['amount']),
            )
            from_transaction.save()
            to_transaction = Transaction(
                account=form.cleaned_data['to_account'],
                date=form.cleaned_data['date'],
                summary="Transfer from %s" % form.cleaned_data['from_account'],
                amount=form.cleaned_data['amount'],
            )
            to_transaction.save()
            # Link the two transactions together
            from_transaction.linked = to_transaction
            from_transaction.save()
            to_transaction.linked = from_transaction
            to_transaction.save()
            return redirect(to_transaction)
    else:
        form = TransferBetweenAccountsForm(request.user, initial={
            'date': now(),
        })
    return render(request, 'form.html', {
        'title': 'Transfer Between Accounts',
        'form': form,
        'description': "Fill in the form below to transfer from one account to another.",
    })


@login_required
def view_transaction(request, id):
    transaction = get_object_or_404(Transaction, pk=id, account__user=request.user)
    return render(request, 'ledger/view_transaction.html', {
        'title': transaction,
        'transaction': transaction,
    })
