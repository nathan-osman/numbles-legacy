from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from numbles.business.models import Invoice


@login_required
def view_invoices(request):
    """
    Show all invoices for the user.
    """
    return render(request, 'business/pages/view_invoices.html', {
        'title': "View Invoices",
        'invoices': Invoice.objects.filter(user=request.user),
    })
