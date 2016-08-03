# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0005_auto_20160723_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantity',
            name='createdAt',
            field=models.DateField(default=datetime.date.today, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='quantity',
            name='transferType',
            field=models.CharField(max_length=20, verbose_name='Transfer Type', choices=[(b'sales', 'Sales'), (b'imports', 'Imports'), (b'transport', 'Transport')]),
        ),
    ]
