# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ledger', '0003_refactor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Descriptive name', max_length=20)),
                ('color', models.CharField(help_text=b'Background color', max_length=7, choices=[(b'#773333', b'Red'), (b'#337733', b'Green'), (b'#333377', b'Blue'), (b'#777733', b'Yellow'), (b'#773377', b'Magenta'), (b'#337777', b'Cyan')])),
                ('user', models.ForeignKey(related_name='tags', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='tags',
            field=models.ManyToManyField(related_name='transactions', to='ledger.Tag', blank=True),
        ),
    ]
