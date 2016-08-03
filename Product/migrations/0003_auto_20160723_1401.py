# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0004_auto_20160722_1503'),
        ('Product', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quntity', models.FloatField(default=0, verbose_name='Quantity')),
                ('transferType', models.CharField(max_length=20, verbose_name='Transfer Type', choices=[(b'sales', 'Sales'), (b'imports', 'Imports'), (b'exports', 'Exports')])),
            ],
            options={
                'verbose_name': 'Quantity',
                'verbose_name_plural': 'Quantities',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=800, null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(upload_to=b'Product/', null=True, verbose_name='photo', blank=True),
        ),
        migrations.AddField(
            model_name='quantity',
            name='fk_Product',
            field=models.ForeignKey(related_name='Product', to='Product.Product'),
        ),
        migrations.AddField(
            model_name='quantity',
            name='fk_location_from',
            field=models.ForeignKey(related_name='From', blank=True, to='Company.Location', null=True),
        ),
        migrations.AddField(
            model_name='quantity',
            name='fk_location_to',
            field=models.ForeignKey(verbose_name='To', to='Company.Location'),
        ),
    ]
