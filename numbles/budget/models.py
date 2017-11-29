from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now

from crontab import CronTab


def validate_cron(value):
    """
    Ensure that value is a valid cron expression
    """
    try:
        CronTab(value)
    except ValueError as e:
        raise ValidationError(str(e))


class Category(models.Model):
    """
    Budget item category
    """

    user = models.ForeignKey(User, related_name='categories')
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    """
    Recurring budget item
    """

    user = models.ForeignKey(User, related_name='items')
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    cron = models.CharField(max_length=40, validators=(validate_cron,))
    next = models.DateTimeField(editable=False)

    amount = models.DecimalField(
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
    )

    # Categories are currently optional for items
    category = models.ForeignKey(Category, blank=True, null=True, related_name='items')

    class Meta:
        ordering = ('next',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('budget:view_item', (), {'id': self.id})

    def total(self, start, end):
        """
        Calculate the total amount for the time range represented by the start
        and end parameters
        """
        a = Decimal('0')
        e = CronTab(self.cron)
        d = start + timedelta(0, e.next(start))
        while d < end:
            a += self.amount
            d += timedelta(0, e.next(d, default_utc=True))
        return a


@receiver(models.signals.pre_save, sender=Item)
def on_item_save(instance, **kwargs):
    """
    Ensure that next is set to the next time the item should run
    """
    n = now()
    instance.next = n + \
        timedelta(0, CronTab(instance.cron).next(n, default_utc=True))

