from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from numbles.ledger.models import Account, Transaction, Year


@login_required
def index(request):
    return render(request, 'pages/index.html', {
        'title': 'Dashboard',
        'home': True,
        'accounts': Account.objects.filter(user=request.user),
        'transactions': Transaction.objects.filter(user=request.user).order_by('-date')[:6],
        'years': Year.objects.filter(user=request.user, account__include_in_balance=True)
            .values('year').annotate(sum=Sum('balance')),
        'stats': {
            'total_accounts': Account.objects.filter(user=request.user).count(),
            'total_transactions': Transaction.objects.filter(user=request.user).count(),
        }
    })
