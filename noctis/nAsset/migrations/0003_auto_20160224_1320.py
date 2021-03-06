# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-24 13:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nPath', '0001_initial'),
        ('nAsset', '0002_auto_20160216_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='nasset',
            name='object_name',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='nasset',
            name='path_setup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nPath.nPath'),
        ),
        migrations.AlterField(
            model_name='nasset',
            name='object_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nAsset.nObjectType'),
        ),
    ]
