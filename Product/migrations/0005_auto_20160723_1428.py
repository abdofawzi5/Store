# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0004_auto_20160723_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantity',
            name='transferType',
            field=models.CharField(max_length=20, verbose_name='Transfer Type', choices=[(b'sales', 'Sales'), (b'imports', 'Imports'), (b'exports', 'Exports'), (b'transport', 'Transport')]),
        ),
    ]
