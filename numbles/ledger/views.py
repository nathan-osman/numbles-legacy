from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware, now

from numbles.ledger.forms import EditAccountForm, DeleteAccountForm, \
    EditTransactionForm, TransferBetweenAccountsForm, DeleteTransactionForm, \
    SearchForm
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
    return render(request, 'pages/form.html', {
        'title': 'Edit "%s"' % account if account else "Add Account",
        'breadcrumbs': [
            account,
        ] if account else [],
        'form': form,
    })


@login_required
def view_account(request, id):
    account = get_object_or_404(Account, pk=id, user=request.user)
    # Calculate the first day of the month one year ago
    n = now()
    start = make_aware(datetime(n.year - 1, (n.month) % 12 + 1, 1))
    # Create a map of [1-indexed month] => [total for the month]
    months = dict([(m, 0) for m in range(1, 13)])
    for t in account.transactions.filter(date__gt=start, date__lte=n):
        months[t.date.month] += t.amount
    return render(request, 'ledger/pages/account_view.html', {
        'title': account,
        'account': account,
        'month': n.month,
        'totals': months.values(),
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
    return render(request, 'pages/form.html', {
        'title': 'Delete "%s"' % account,
        'breadcrumbs': [
            account,
        ],
        'form': form,
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
    return render(request, 'pages/form.html', {
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
    return render(request, 'pages/form.html', {
        'title': 'Transfer Between Accounts',
        'form': form,
    })


@login_required
def view_transaction(request, id):
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)
    return render(request, 'ledger/pages/transaction_view.html', {
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
    return render(request, 'pages/form.html', {
        'title': 'Delete "%s"' % transaction,
        'breadcrumbs': [
            transaction.account,
            transaction,
        ],
        'form': form,
    })


@login_required
def view_year(request, year):
    # Sum the balance of all previous years and use that as the initial value
    balance = request.user.years.filter(year__lt=year).aggregate(sum=Sum('balance'))
    transactions = request.user.transactions.filter(year__year=year)
    return render(request, 'ledger/pages/view_year.html', {
        'title': 'Year: %s' % year,
        'transactions': transactions,
        'balance': balance['sum'] or 0,
    })


@login_required
def search(request):
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            q = form.cleaned_data['query']
            transactions = Transaction.objects.filter(
                Q(summary__icontains=q) | Q(description__icontains=q),
                user=request.user,
            )
            return render(request, 'ledger/pages/search.html', {
                'title': 'Search Results for "%s"' % q,
                'transactions': transactions,
            })
    else:
        form = SearchForm()
    return render(request, 'pages/form.html', {
        'title': 'Search',
        'form': form,
    })
