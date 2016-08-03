# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0006_auto_20160724_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quantity',
            name='createdAt',
        ),
        migrations.AddField(
            model_name='quantity',
            name='the_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]
