from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from numbles.business.forms import EditClientForm, EditInvoiceForm
from numbles.business.models import Client, Invoice
from numbles.forms import DeleteForm


@login_required
def index(request):
    """
    Show a list of "current" data
    """
    return render(request, 'business/pages/index.html', {
        'title': "Business",
    })


@login_required
def view_clients(request):
    """
    Show all clients
    """
    return render(request, 'business/pages/view_clients.html', {
        'title': "View Clients",
        'clients': Client.objects.filter(user=request.user),
    })


@login_required
def edit_client(request, id=None):
    """
    Edit a client
    """
    client = id and get_object_or_404(Client, pk=id, user=request.user)
    if request.method == 'POST':
        form = EditClientForm(instance=client, data=request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            return redirect(client)
    else:
        form = EditClientForm(instance=client)
    return render(request, 'pages/form.html', {
        'title': "{} Client".format("Edit" if id else "New"),
        'form': form,
    })


@login_required
def view_client(request, id):
    client = get_object_or_404(Client, pk=id, user=request.user)
    return render(request, 'business/pages/view_client.html', {
        'title': client,
        'client': client,
    })


@login_required
def delete_client(request, id):
    client = get_object_or_404(Client, pk=id, user=request.user)
    if request.method == 'POST':
        form = DeleteForm(data=request.POST)
        if form.is_valid():
            client.delete()
            return redirect('business:view_clients')
    else:
        form = DeleteForm()
    return render(request, 'pages/delete.html', {
        'title': "Delete Client",
        'description': "You are about to delete {}".format(client),
        'breadcrumbs': [client],
        'form': form,
        'related': client.invoices.all(),
    })


@login_required
def view_invoices(request):
    """
    Show all invoices for the user.
    """
    return render(request, 'business/pages/view_invoices.html', {
        'title': "View Invoices",
        'invoices': Invoice.objects.filter(user=request.user),
    })


@login_required
def edit_invoice(request, id=None):
    """
    Edit an invoice
    """
    invoice = id and get_object_or_404(Invoice, pk=id, user=request.user)
    if request.method == 'POST':
        form = EditInvoiceForm(instance=invoice, data=request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            return redirect(invoice)
    else:
        initial = {}
        if not invoice:
            initial['date'] = now()
        form = EditInvoiceForm(instance=invoice, initial=initial)
    return render(request, 'pages/form.html', {
        'title': "{} Invoice".format("Edit" if id else "New"),
        'form': form,
    })


@login_required
def view_invoice(request, id):
    pass
