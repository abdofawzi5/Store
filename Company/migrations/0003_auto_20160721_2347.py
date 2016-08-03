# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0002_auto_20160721_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='Company Name')),
                ('photo', models.ImageField(upload_to=b'location_logo/', null=True, verbose_name='photo', blank=True)),
                ('description', models.CharField(max_length=100, null=True, verbose_name='Short Description', blank=True)),
                ('Mission', models.CharField(max_length=800, null=True, verbose_name='Mission', blank=True)),
                ('createdAt', models.DateField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='LocationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=20, verbose_name='Location Type')),
            ],
            options={
                'verbose_name': 'Location Type',
                'verbose_name_plural': 'Location Types',
            },
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.RemoveField(
            model_name='company',
            name='fk_use',
        ),
        migrations.AddField(
            model_name='location',
            name='fk_locationType',
            field=models.ForeignKey(verbose_name='openSince', to='Company.LocationType'),
        ),
    ]
