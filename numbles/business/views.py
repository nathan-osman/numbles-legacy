from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from numbles.business.forms import EditClientForm, EditEntryForm, \
    EditInvoiceForm
from numbles.business.models import Client, Entry, Invoice
from numbles.business.pdf import InvoiceGenerator
from numbles.forms import DeleteForm


@login_required
def view_clients(request):
    """
    Show all clients
    """
    q = Client.objects.filter(user=request.user).annotate(
        num_invoices=models.Count('invoices'),
        num_unpaid_invoices=models.Sum(
            models.Case(
                models.When(invoices__status=Invoice.ISSUED, then=1),
                default=0,
                output_field=models.IntegerField(),
            ),
        ),
    )
    return render(request, 'business/pages/view_clients.html', {
        'title': "View Clients",
        'clients': q,
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
            m = Invoice.objects.all().aggregate(m=models.Max('id'))['m']
            initial['id'] = (m or 0) + 1
            initial['client'] = request.GET.get('client', None)
            initial['date'] = now()
        form = EditInvoiceForm(instance=invoice, initial=initial)
    return render(request, 'pages/form.html', {
        'title': "{} Invoice".format("Edit" if id else "New"),
        'form': form,
    })


@login_required
def view_invoice(request, id):
    invoice = get_object_or_404(Invoice, pk=id, user=request.user)
    return render(request, 'business/pages/view_invoice.html', {
        'title': invoice,
        'invoice': invoice,
    })


@login_required
def delete_invoice(request, id):
    invoice = get_object_or_404(Invoice, pk=id, user=request.user)
    if request.method == 'POST':
        form = DeleteForm(data=request.POST)
        if form.is_valid():
            invoice.delete()
            return redirect('business:view_invoices')
    else:
        form = DeleteForm()
    return render(request, 'pages/delete.html', {
        'title': "Delete Invoice",
        'description': "You are about to delete {}".format(invoice),
        'form': form,
        'related': invoice.entries.all(),
    })


@login_required
def pdf(request, id):
    invoice = get_object_or_404(Invoice, pk=id, user=request.user)
    response = HttpResponse(content_type='application/pdf')
    if 'download' in request.GET:
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(unicode(invoice))
    InvoiceGenerator(response, invoice).generate()
    return response


@login_required
def edit_entry(request, id=None):
    entry = id and get_object_or_404(Entry, pk=id, invoice__user=request.user)
    if request.method == 'POST':
        form = EditEntryForm(request.user, instance=entry, data=request.POST)
        if form.is_valid():
            entry = form.save()
            return redirect(entry.invoice)
    else:
        initial = {}
        if not entry:
            initial['invoice'] = request.GET.get('invoice', None)
        form = EditEntryForm(request.user, instance=entry, initial=initial)
    return render(request, 'pages/form.html', {
        'title': "{} Entry".format("Edit" if id else "New"),
        'breadcrumbs': [entry.invoice] if entry else [],
        'form': form,
    })


@login_required
def delete_entry(request, id):
    entry = get_object_or_404(Entry, pk=id, invoice__user=request.user)
    if request.method == 'POST':
        form = DeleteForm(data=request.POST)
        if form.is_valid():
            entry.delete()
            return redirect(entry.invoice)
    else:
        form = DeleteForm()
    return render(request, 'pages/delete.html', {
        'title': "Delete Entry",
        'description': "You are about to delete {}".format(entry),
        'form': form,
    })
