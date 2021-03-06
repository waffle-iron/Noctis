# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-15 12:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import noctis.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nTracking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='nStatusComponentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_id', models.IntegerField(default=0)),
                ('modified_on', models.DateTimeField(default=datetime.datetime.now)),
                ('status_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nTracking.nStatusComponentLevel')),
            ],
        ),
        migrations.AddField(
            model_name='nstatustype',
            name='status_breakdown',
            field=noctis.fields.ListField(null=True),
        ),
        migrations.AddField(
            model_name='nstatustype',
            name='total_status_components',
            field=models.IntegerField(default=0),
        ),
    ]
