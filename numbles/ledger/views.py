from datetime import datetime
from json import dumps

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware, now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from numbles.forms import DeleteForm
from numbles.ledger.exporters import export as export_transactions
from numbles.ledger.forms import AttachForm, EditAccountForm, EditTagForm, \
    EditTransactionForm, LinkForm, ToggleForm, TransferForm
from numbles.ledger.models import Account, Attachment, Tag, Transaction
from numbles.ledger.util import parse_transaction_form


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
        'title': "{} Account".format("Edit" if account else "New"),
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
        months.append({
            'url': reverse('ledger:view_month', kwargs={
                'year': y,
                'month': m,
            }),
            'year': y,
            'month': m,
            'amount': str(Transaction.month(y, m, account=account).sum()),
        })
    return render(request, 'ledger/pages/view_account.html', {
        'title': account,
        'account': account,
        'months': dumps(months),
    })


@login_required
def delete_account(request, id):
    """
    Delete an account.
    """
    account = get_object_or_404(Account, pk=id, user=request.user)
    if request.method == 'POST':
        form = DeleteForm(data=request.POST)
        if form.is_valid():
            account.delete()
            return redirect('home')
    else:
        form = DeleteForm()
    return render(request, 'pages/delete.html', {
        'title': "Delete Account",
        'description': "You are about to delete {}.".format(account),
        'breadcrumbs': [account],
        'form': form,
        'related': account.transactions.all(),
    })


@login_required
def delete_attachment(request, id):
    """
    Delete an attachment.
    """
    attachment = get_object_or_404(Attachment, pk=id, transaction__user=request.user)
    if request.method == 'POST':
        form = DeleteForm(data=request.POST)
        if form.is_valid():
            attachment.delete()
            return redirect(attachment.transaction)
    else:
        form = DeleteForm()
    return render(request, 'pages/delete.html', {
        'title': "Delete Attachment",
        'description': "You are about to delete {}.".format(attachment),
        'breadcrumbs': [attachment.transaction.account, attachment.transaction],
        'form': form,
    })


@login_required
def edit_tag(request, id=None):
    """
    Create or edit a tag.
    """
    tag = id and get_object_or_404(Tag, pk=id, user=request.user)
    if request.method == 'POST':
        form = EditTagForm(instance=tag, data=request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(tag)
    else:
        form = EditTagForm(instance=tag)
    return render(request, 'pages/form.html', {
        'title': "{} Tag".format("Edit" if tag else "New"),
        'form': form,
    })


@login_required
def delete_tag(request, id):
    """
    Delete a tag.
    """
    tag = get_object_or_404(Tag, pk=id, user=request.user)
    if request.method == 'POST':
        form = DeleteForm(data=request.POST)
        if form.is_valid():
            tag.delete()
            return redirect('home')
    else:
        form = DeleteForm()
    return render(request, 'pages/delete.html', {
        'title': "Delete Tag",
        'description': "You are about to remove the {} tag from all transactions and delete it.".format(tag),
        'form': form,
    })


@login_required
def transactions(request):
    """
    Fully customizable transaction list
    """
    form, t = parse_transaction_form(request)
    return render(request, 'ledger/pages/transactions.html', {
        'title': "Transactions",
        'transactions': t,
        'form': form,
    })


@login_required
@transaction.atomic
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
            form.save_m2m()
            return redirect(transaction)
    else:
        initial = {}
        if not transaction:
            duplicate_id = request.GET.get('duplicate_id', None)
            if duplicate_id is not None:
                initial = get_object_or_404(Transaction, pk=duplicate_id, user=request.user).__dict__
            else:
                initial['account'] = request.GET.get('account', None)
                initial['date'] = now()
        form = EditTransactionForm(request.user, instance=transaction, initial=initial)
    return render(request, 'pages/form.html', {
        'title': "{} Transaction".format("Edit" if transaction else "New"),
        'breadcrumbs': [transaction.account, transaction] if transaction else [],
        'form': form,
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
            )
            to_transaction.save()
            to_transaction.links.add(from_transaction)
            to_transaction.save()
            from_transaction.links.add(to_transaction)
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
def link(request, id):
    """
    Link a transaction.
    """
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)
    if request.method == 'POST':
        form = LinkForm(request.user, data=request.POST)
        if form.is_valid():
            transaction.links.add(form.cleaned_data['transaction_id'])
            transaction.save()
            return redirect(transaction)
    else:
        form = LinkForm(request.user)
    return render(request, "pages/form.html", {
        'title': "Link Transaction",
        'description': "Enter the ID of a transaction to link.",
        'breadcrumbs': [transaction.account, transaction],
        'form': form,
    })


@login_required
def unlink(request, id, id2):
    """
    Unlink a transaction
    """
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)
    transaction2 = get_object_or_404(Transaction, pk=id2, user=request.user)
    if request.method == 'POST':
        form = DeleteForm(data=request.POST)
        if form.is_valid():
            transaction.links.remove(transaction2)
            transaction.save()
            return redirect(transaction)
    else:
        form = DeleteForm()
    return render(request, 'pages/delete.html', {
        'title': "Unlink Transaction",
        'description': "You are about to unlink {}. Links will be removed in both directions.".format(transaction2),
        'breadcrumbs': [transaction.account, transaction],
        'form': form,
    })


@login_required
def attach(request, id):
    """
    Attach a file to a transaction.
    """
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)
    if request.method == 'POST':
        form = AttachForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            a = form.save(commit=False)
            a.transaction = transaction
            a.save()
            return redirect(transaction)
    else:
        form = AttachForm()
    return render(request, 'pages/form.html', {
        'title': "Attach File",
        'description': "You are about to attach a file to {}.".format(transaction),
        'breadcrumbs': [transaction.account, transaction],
        'form': form,
    })


@login_required
def delete_transaction(request, id):
    """
    Delete a transaction.
    """
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)
    if request.method == 'POST':
        form = DeleteForm(data=request.POST)
        if form.is_valid():
            transaction.delete()
            return redirect(transaction.account)
    else:
        form = DeleteForm()
    return render(request, 'pages/delete.html', {
        'title': "Delete Transaction",
        'description': "You are about to delete {}.".format(transaction),
        'breadcrumbs': [transaction.account, transaction],
        'form': form,
    })


@login_required
def export(request):
    form, t = parse_transaction_form(request)
    return export_transactions(request.GET.get('format', ''), t)


@login_required
@csrf_exempt
@require_POST
def toggle_transaction(request):
    """
    Toggle the reconciled status of a transaction
    """
    form = ToggleForm(request.user, data=request.POST)
    if form.is_valid():
        t = form.cleaned_data['transaction']
        t.reconciled = not t.reconciled
        t.save()
        return JsonResponse({
            'reconciled': t.reconciled,
        })
    else:
        return JsonResponse({
            'error': "invalid transaction",
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
        date__lt=start,
    ).sum()
    return render(request, 'ledger/pages/view_month.html', {
        'title': start.strftime('%B %Y'),
        'transactions': transactions,
        'balance': balance,
        'prev_month': adjust_month(year, month, -1),
        'next_month': adjust_month(year, month, 1),
    })
