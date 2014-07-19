from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from numbles.ledger.models import Account


@login_required
def index(request):
    """Render the home page."""
    return render(request, 'index.html', {
        'title': 'Dashboard',
        'home': True,
        'accounts': Account.objects.filter(user=request.user),
    })
