# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0004_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('summary', models.CharField(help_text=b'Brief description of the attachment', max_length=100)),
                ('file', models.FileField(upload_to=b'attachments')),
                ('transaction', models.ForeignKey(related_name='attachments', to='ledger.Transaction')),
            ],
            options={
                'ordering': ('summary',),
            },
        ),
    ]
