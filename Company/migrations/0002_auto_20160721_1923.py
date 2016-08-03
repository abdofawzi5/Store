# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='height',
        ),
        migrations.AddField(
            model_name='company',
            name='Mission',
            field=models.CharField(max_length=800, null=True, verbose_name='Mission', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to=b'company_logo/', null=True, verbose_name='Logo', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='long_description',
            field=models.CharField(max_length=800, null=True, verbose_name='Long Description', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='short_description',
            field=models.CharField(max_length=100, null=True, verbose_name='Short Description', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='slogan',
            field=models.CharField(max_length=50, null=True, verbose_name='Slogan', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Company Name'),
        ),
    ]
