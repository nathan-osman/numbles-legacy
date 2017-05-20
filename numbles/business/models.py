from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


class Client(models.Model):
    """
    Client for whom work is completed.
    """

    user = models.ForeignKey(User, related_name='clients')

    name = models.CharField(max_length=40, help_text="Client business name")
    address = models.TextField(help_text="Client business address")

    def __unicode__(self):
        return self.name


class Invoice(models.Model):
    """
    Invoice used for billing clients for work completed
    """

    user = models.ForeignKey(User, related_name='invoices')
    client = models.ForeignKey(Client, related_name='invoices')

    date = models.DateField(help_text="Date of invoice issuance")
    amount = models.DecimalField(
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        default=Decimal('0.00'),
    )

    def __unicode__(self):
        return "{:03d}".format(self.id)


class Entry(models.Model):
    """
    Individual work item completed for an invoice
    """

    invoice = models.ForeignKey(Invoice, related_name='entries')

    description = models.TextField()

    amount = models.DecimalField(
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        default=Decimal('0.00'),
    )

    class Meta:
        verbose_name_plural = "entries"

    def __unicode__(self):
        return self.invoice


@receiver(models.signals.post_init, sender=Entry)
def on_entry_init(instance, **kwargs):
    instance.original_amount = instance.amount if instance.id else Decimal('0.00')


@receiver(models.signals.post_save, sender=Entry)
def on_entry_save(instance, created, **kwargs):
    instance.invoice.amount += instance.amount - instance.original_amount
    instance.invoice.save()


@receiver(models.signals.post_delete, sender=Entry)
def on_entry_delete(instance, **kwargs):
    instance.invoice.amount -= instance.amount
    instance.invoice.save()
