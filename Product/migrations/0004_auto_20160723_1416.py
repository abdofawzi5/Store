# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_auto_20160723_1401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quantity',
            old_name='quntity',
            new_name='quantity',
        ),
        migrations.AddField(
            model_name='product',
            name='createdAt',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Created At', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quantity',
            name='createdAt',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Created At', auto_now=True),
            preserve_default=False,
        ),
    ]
