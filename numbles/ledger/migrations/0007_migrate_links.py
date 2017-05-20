# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 03:35
from __future__ import unicode_literals

from django.db import migrations


def migrate_links(apps, schema_editor):
    """
    Create the many-to-many relationships for each of the existing linked
    transactions.
    """
    Transaction = apps.get_model('ledger', 'Transaction')
    for t in Transaction.objects.all():
        if t.linked:
            t.links.add(t.linked)
            t.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0006_transaction_links'),
    ]

    operations = [
        migrations.RunPython(migrate_links),
    ]
