# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0004_auto_20160722_1503'),
        ('Product', '0007_auto_20160724_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField(default=0, verbose_name='Quantity')),
                ('price', models.FloatField(default=0, null=True, verbose_name='Total Price', blank=True)),
                ('the_date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('fk_location_to', models.ForeignKey(verbose_name='To', to='Company.Location')),
                ('fk_product', models.ForeignKey(related_name='Product', to='Product.Product')),
            ],
            options={
                'verbose_name': 'Import',
                'verbose_name_plural': 'Imports',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField(default=0, verbose_name='Quantity')),
                ('price', models.FloatField(default=0, verbose_name='Price')),
                ('bill', models.ImageField(upload_to=b'bill/', null=True, verbose_name='bill', blank=True)),
                ('the_date', models.DateField(default=datetime.date.today, verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField(default=0, verbose_name='Quantity')),
                ('price', models.FloatField(default=0, verbose_name='Price per Item')),
                ('discount_rate', models.FloatField(default=0, verbose_name='Discount Rate', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('the_date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('fk_import', models.ForeignKey(related_name='Imports', to='Product.Imports')),
                ('fk_location_from', models.ForeignKey(related_name='From', to='Company.Location', null=True)),
                ('fk_location_to', models.ForeignKey(verbose_name='To', to='Company.Location')),
            ],
            options={
                'verbose_name': 'Transfer',
                'verbose_name_plural': 'Transfers',
            },
        ),
        migrations.RemoveField(
            model_name='quantity',
            name='fk_Product',
        ),
        migrations.RemoveField(
            model_name='quantity',
            name='fk_location_from',
        ),
        migrations.RemoveField(
            model_name='quantity',
            name='fk_location_to',
        ),
        migrations.DeleteModel(
            name='Quantity',
        ),
        migrations.AddField(
            model_name='sales',
            name='fk_transfer',
            field=models.ForeignKey(related_name='Transfers', to='Product.Transfers'),
        ),
    ]
