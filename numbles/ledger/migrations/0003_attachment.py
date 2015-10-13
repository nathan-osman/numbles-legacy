# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0002_account_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(help_text=b'Brief description of the attachment.', max_length=100)),
                ('attachment', models.FileField(help_text=b'File to be uploaded.', upload_to=b'attachments')),
                ('transaction', models.ForeignKey(related_name='attachments', to='ledger.Transaction')),
            ],
        ),
    ]
