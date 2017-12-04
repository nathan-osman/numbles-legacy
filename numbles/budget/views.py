from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import localtime, make_aware, now

from ..forms import DeleteForm
from .forms import EditItemForm
from .models import Item


@login_required
def index(request):
    n = localtime(now())
    s = make_aware(datetime(n.year, 1, 1))
    e = make_aware(datetime(n.year + 1, 1, 1))
    return render(request, 'budget/pages/index.html', {
        'title': "Budget",
        'items': Item.objects.filter(user=request.user),
        'start': s,
        'end': e,
    })


@login_required
def view_item(request, id):
    """
    View an item
    """
    item = get_object_or_404(Item, pk=id, user=request.user)
    return render(request, 'budget/pages/view_item.html', {
        'title': item.name,
        'item': item,
    })


@login_required
def edit_item(request, id=None):
    """
    Edit an item
    """
    item = id and get_object_or_404(Item, pk=id, user=request.user)
    if request.method == 'POST':
        form = EditItemForm(instance=item, data=request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect(item)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'budget/pages/edit_item.html', {
        'title': "{} Item".format("Edit" if id else "New"),
        'form': form,
    })


@login_required
def delete_item(request, id):
    """
    Delete an item
    """
    item = get_object_or_404(Item, pk=id, user=request.user)
    if request.method == 'POST':
        form = DeleteForm(data=request.POST)
        if form.is_valid():
            item.delete()
            return redirect('budget:index')
    else:
        form = DeleteForm()
    return render(request, 'pages/delete.html', {
        'title': "Delete Item",
        'description': "You are about to delete {}".format(item),
        'breadcrumbs': [item],
        'form': form,
    })
