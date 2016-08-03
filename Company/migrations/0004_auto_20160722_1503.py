# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0003_auto_20160721_2347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='location',
            name='fk_locationType',
            field=models.ForeignKey(verbose_name='Location Type', to='Company.LocationType'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Name'),
        ),
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
