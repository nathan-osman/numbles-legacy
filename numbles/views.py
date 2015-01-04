from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from numbles.ledger.models import Account, Year


@login_required
def index(request):
    return render(request, 'index.html', {
        'title': 'Dashboard',
        'home': True,
        'accounts': Account.objects.filter(user=request.user),
        'years': Year.objects.filter(user=request.user, account__include_in_balance=True)
            .values('year').annotate(sum=Sum('balance')),
    })
