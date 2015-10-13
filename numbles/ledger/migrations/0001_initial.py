# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
from django.conf import settings
import numbles.ledger.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2)),
                ('name', models.CharField(help_text=b'Account name.', max_length=40)),
                ('include_in_balance', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-balance', 'name'),
            },
            bases=(models.Model, numbles.ledger.models.UpdateMixin),
        ),
        migrations.CreateModel(
            name='Total',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('balance', models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model, numbles.ledger.models.UpdateMixin),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(help_text=b'Date and time of the transaction.')),
                ('summary', models.CharField(help_text=b'Brief description of the transaction.', max_length=100)),
                ('description', models.TextField(help_text=b'Additional details or information.', blank=True)),
                ('amount', models.DecimalField(help_text=b'Amount of the transaction.', max_digits=9, decimal_places=2)),
                ('reconciled', models.BooleanField(default=False)),
                ('account', models.ForeignKey(related_name='transactions', to='ledger.Account')),
                ('linked', models.ForeignKey(blank=True, to='ledger.Transaction', null=True)),
                ('user', models.ForeignKey(related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.DecimalField(default=Decimal('0.00'), max_digits=9, decimal_places=2)),
                ('year', models.PositiveSmallIntegerField()),
                ('account', models.ForeignKey(related_name='years', to='ledger.Account')),
                ('user', models.ForeignKey(related_name='years', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('year',),
            },
            bases=(models.Model, numbles.ledger.models.UpdateMixin),
        ),
        migrations.AddField(
            model_name='transaction',
            name='year',
            field=models.ForeignKey(related_name='transactions', to='ledger.Year'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='total',
            field=models.ForeignKey(related_name='accounts', to='ledger.Total'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(related_name='accounts', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
