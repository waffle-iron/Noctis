# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-24 04:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nProject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nproject',
            name='short',
            field=models.CharField(default='', max_length=10),
        ),
    ]
