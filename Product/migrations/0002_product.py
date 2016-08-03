# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='Company Name')),
                ('photo', models.ImageField(upload_to=b'location_logo/', null=True, verbose_name='photo', blank=True)),
                ('description', models.CharField(max_length=800, null=True, verbose_name='Short Description', blank=True)),
                ('price', models.FloatField(default=0, null=True, verbose_name='Price', blank=True)),
                ('fk_category', models.ForeignKey(verbose_name='Category', to='Product.Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
