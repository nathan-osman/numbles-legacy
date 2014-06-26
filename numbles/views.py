from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    """Render the home page."""
    return render(request, 'index.html', {
        'title': 'Dashboard',
    })
