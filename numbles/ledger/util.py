from django.db.models import Q

from numbles.ledger.forms import TransactionForm
from numbles.ledger.models import Transaction


def parse_transaction_form(request):
    """
    Convert a dict of parameters to a queryset.
    """
    t = Transaction.objects.filter(user=request.user)
    form = TransactionForm(request.user, data=request.GET)
    if form.is_valid():
        date_from = form.cleaned_data['date_from']
        if date_from is not None:
            t = t.filter(date__gte=date_from)
        date_to = form.cleaned_data['date_to']
        if date_to is not None:
            t = t.filter(date__lte=date_to)
        q = form.cleaned_data['query']
        if q is not None:
            t = t.filter(Q(summary__icontains=q) | Q(description__icontains=q))
        account = form.cleaned_data['account']
        if account is not None:
            t = t.filter(account=account)
        tag = form.cleaned_data['tag']
        if tag is not None:
            t = t.filter(tags=tag)
        reconciled = form.cleaned_data['reconciled']
        if reconciled is not None:
            t = t.filter(reconciled=reconciled)
        amount_min = form.cleaned_data['amount_min']
        if amount_min is not None:
            t = t.filter(amount__gte=amount_min)
        amount_max = form.cleaned_data['amount_max']
        if amount_max is not None:
            t = t.filter(amount__lte=amount_max)
        has_attachment = form.cleaned_data['has_attachment']
        if has_attachment is not None:
            if has_attachment:
                t = t.filter(~Q(attachments=None))
            else:
                t = t.filter(attachments=None)
    return form, t
