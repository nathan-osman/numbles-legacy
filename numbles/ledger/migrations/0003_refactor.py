# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0002_account_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='total',
            name='user',
        ),
        migrations.RemoveField(
            model_name='year',
            name='account',
        ),
        migrations.RemoveField(
            model_name='year',
            name='user',
        ),
        migrations.RemoveField(
            model_name='account',
            name='total',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='year',
        ),
        migrations.DeleteModel(
            name='Total',
        ),
        migrations.DeleteModel(
            name='Year',
        ),
    ]
