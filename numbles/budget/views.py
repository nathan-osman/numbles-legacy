from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Item


@login_required
def index(request):
    return render(request, 'budget/pages/index.html', {
        'title': "Budget",
        'items': Item.objects.filter(user=request.user),
    })
