from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from numbles.ledger.forms import EditAccountForm, DeleteAccountForm, \
    EditTransactionForm, TransferBetweenAccountsForm, DeleteTransactionForm
from numbles.ledger.models import Account, Transaction


@login_required
def edit_account(request, id=None):
    account = id and get_object_or_404(Account, pk=id, user=request.user)
    if request.method == 'POST':
        form = EditAccountForm(instance=account, data=request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.total = request.user.total
            account.save()
            return redirect(account)
    else:
        form = EditAccountForm(instance=account)
    return render(request, 'form.html', {
        'title': 'Edit "%s"' % account if account else "Add Account",
        'breadcrumbs': [
            account,
        ] if account else [],
        'form': form,
    })


@login_required
def view_account(request, id):
    account = get_object_or_404(Account, pk=id, user=request.user)
    return render(request, 'ledger/view_account.html', {
        'title': account,
        'account': account,
    })


@login_required
def delete_account(request, id):
    account = get_object_or_404(Account, pk=id, user=request.user)
    if request.method == 'POST':
        form = DeleteAccountForm(data=request.POST)
        if form.is_valid():
            account.delete()
            return redirect('home')
    else:
        form = DeleteAccountForm()
    return render(request, 'form.html', {
        'title': 'Delete "%s"' % account,
        'breadcrumbs': [
            account,
        ],
        'form': form,
    })


@login_required
def transactions(request):
    return render(request, 'ledger/transactions.html', {
        'title': 'Transactions',
        'transactions': Transaction.objects.all(),
    })


@login_required
def edit_transaction(request, id=None):
    transaction = id and get_object_or_404(Transaction, pk=id, user=request.user)
    if request.method == 'POST':
        form = EditTransactionForm(request.user, instance=transaction, data=request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect(transaction)
    else:
        initial = {} if transaction else {'date': now()}
        form = EditTransactionForm(request.user, instance=transaction, initial=initial)
    return render(request, 'form.html', {
        'title': 'Edit "%s"' % transaction if transaction else "Add Transaction",
        'breadcrumbs': [
            transaction.account,
            transaction,
        ] if transaction else [],
        'form': form,
    })


@login_required
@transaction.atomic
def transfer(request):
    if request.method == 'POST':
        form = TransferBetweenAccountsForm(request.user, data=request.POST)
        if form.is_valid():
            # Create the "from" transaction
            from_transaction = Transaction(
                user=request.user,
                account=form.cleaned_data['from_account'],
                date=form.cleaned_data['date'],
                summary="Transfer to %s" % form.cleaned_data['to_account'],
                amount=-form.cleaned_data['amount']
            )
            from_transaction.save()
            # Create the "to" transaction
            to_transaction = Transaction(
                user=request.user,
                account=form.cleaned_data['to_account'],
                date=form.cleaned_data['date'],
                summary="Transfer from %s" % form.cleaned_data['from_account'],
                amount=form.cleaned_data['amount'],
                linked=from_transaction
            )
            to_transaction.save()
            # This must be done separately due to circular reference
            from_transaction.linked = to_transaction
            from_transaction.save()
            return redirect(to_transaction)
    else:
        form = TransferBetweenAccountsForm(request.user, initial={
            'date': now(),
        })
    return render(request, 'form.html', {
        'title': 'Transfer Between Accounts',
        'form': form,
    })


@login_required
def view_transaction(request, id):
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)
    return render(request, 'ledger/view_transaction.html', {
        'title': transaction,
        'breadcrumbs': [
            transaction.account,
        ],
        'transaction': transaction,
    })


@login_required
def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)
    if request.method == 'POST':
        form = DeleteTransactionForm(data=request.POST)
        if form.is_valid():
            transaction.delete()
            return redirect(transaction.account)
    else:
        form = DeleteTransactionForm()
    return render(request, 'form.html', {
        'title': 'Delete "%s"' % transaction,
        'breadcrumbs': [
            transaction.account,
            transaction,
        ],
        'form': form,
    })
