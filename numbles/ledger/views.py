from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware, now

from numbles.ledger.forms import DeleteAccountForm, DeleteTransactionForm, \
    EditAccountForm, EditTransactionForm, FindTransactionForm, TransferForm
from numbles.ledger.models import Account, Transaction


@login_required
def edit_account(request, id=None):
    """
    Create or edit an account.
    """
    account = id and get_object_or_404(Account, pk=id, user=request.user)
    if request.method == 'POST':
        form = EditAccountForm(instance=account, data=request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect(account)
    else:
        form = EditAccountForm(instance=account)
    return render(request, 'pages/form.html', {
        'title': "Edit {}".format(account) if account else "New Account",
        'breadcrumbs': [account] if account else [],
        'form': form,
    })


def adjust_month(year, month, offset):
    """
    Given a year and month, add the specified offset and return a tuple in the
    form (year, month). The algorithm is a bit complicated because month
    indices begin at 1 instead of 0.
    """
    month += offset - 1
    year += month / 12
    month = month % 12 + 1
    return (year, month)


@login_required
def view_account(request, id):
    """
    View summary information for an account. The graph displayed along the top
    of the page shows income graphed over the previous year.
    """
    account = get_object_or_404(Account, pk=id, user=request.user)
    months, n = [], now()
    for o in reversed(range(0, -12, -1)):
        y, m = adjust_month(n.year, n.month, o)
        months.append((y, m, Transaction.month(y, m, account=account).sum()))
    return render(request, 'ledger/pages/view_account.html', {
        'title': account,
        'account': account,
        'cur': (n.year, n.month),
        'months': months,
    })


@login_required
def delete_account(request, id):
    """
    Delete an account.
    """
    account = get_object_or_404(Account, pk=id, user=request.user)
    if request.method == 'POST':
        form = DeleteAccountForm(data=request.POST)
        if form.is_valid():
            account.delete()
            return redirect('home')
    else:
        form = DeleteAccountForm()
    return render(request, 'pages/form.html', {
        'title': "Delete {}".format(account),
        'breadcrumbs': [account],
        'form': form,
    })


@login_required
def edit_transaction(request, id=None):
    """
    Create or edit a transaction.
    """
    transaction = id and get_object_or_404(Transaction, pk=id, user=request.user)
    if request.method == 'POST':
        form = EditTransactionForm(request.user, instance=transaction, data=request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect(transaction)
    else:
        initial = {}
        if not transaction:
            initial['account'] = request.GET.get('account', None)
            initial['date'] = now()
        form = EditTransactionForm(request.user, instance=transaction, initial=initial)
    return render(request, 'pages/form.html', {
        'title': "Edit {}".format(transaction) if transaction else "New Transaction",
        'breadcrumbs': [transaction.account, transaction] if transaction else [],
        'form': form,
    })


@login_required
def find_transaction(request):
    """
    Find a transaction.
    """
    transactions = None
    if request.method == 'POST':
        form = FindTransactionForm(request.user, data=request.POST)
        if form.is_valid():
            filters = {'user': request.user}
            account = form.cleaned_data['account']
            if account is not None:
                filters['account'] = account
            tag = form.cleaned_data['tag']
            if tag is not None:
                filters['tags'] = tag
            q = form.cleaned_data['query']
            transactions = Transaction.objects.filter(
                Q(summary__icontains=q) | Q(description__icontains=q),
                **filters
            )
    else:
        form = FindTransactionForm(request.user)
    return render(request, 'ledger/pages/find_transaction.html', {
        'title': "Find Transaction",
        'form': form,
        'transactions': transactions,
    })


@login_required
@transaction.atomic
def transfer(request):
    """
    Transfer an amount between accounts.
    """
    if request.method == 'POST':
        form = TransferForm(request.user, data=request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            date = form.cleaned_data['date']
            amount = form.cleaned_data['amount']
            from_transaction = Transaction(
                user=request.user,
                account=from_account,
                date=date,
                summary="Transfer to {}".format(to_account),
                amount=-amount,
            )
            from_transaction.save()
            to_transaction = Transaction(
                user=request.user,
                account=to_account,
                date=date,
                summary="Transfer from {}".format(from_account),
                amount=amount,
                linked=from_transaction,
            )
            to_transaction.save()
            from_transaction.linked = to_transaction
            from_transaction.save()
            return redirect(to_transaction)
    else:
        form = TransferForm(request.user, initial={'date': now()})
    return render(request, 'pages/form.html', {
        'title': "Transfer",
        'form': form,
    })


@login_required
def view_transaction(request, id):
    """
    View transaction information.
    """
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)
    return render(request, 'ledger/pages/view_transaction.html', {
        'title': transaction,
        'breadcrumbs': [transaction.account],
        'transaction': transaction,
    })


@login_required
def delete_transaction(request, id):
    """
    Delete a transaction.
    """
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)
    if request.method == 'POST':
        form = DeleteTransactionForm(data=request.POST)
        if form.is_valid():
            transaction.delete()
            return redirect(transaction.account)
    else:
        form = DeleteTransactionForm()
    return render(request, 'pages/form.html', {
        'title': "Delete {}".format(transaction),
        'breadcrumbs': [transaction.account, transaction],
        'form': form,
    })


@login_required
def view_month(request, year, month):
    """
    View transactions for a specific month.
    """
    year, month = int(year), int(month)
    transactions = Transaction.month(
        year,
        month,
        user=request.user,
        account__include_in_balance=True,
    )
    start = make_aware(datetime(year, month, 1))
    balance = Transaction.objects.filter(
        user=request.user,
        account__include_in_balance=True,
        date__lt=start
    ).sum()
    return render(request, 'ledger/pages/view_month.html', {
        'title': start.strftime('%B %Y'),
        'transactions': transactions,
        'balance': balance,
        'prev_month': adjust_month(year, month, -1),
        'next_month': adjust_month(year, month, 1),
    })
