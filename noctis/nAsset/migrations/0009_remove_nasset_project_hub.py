# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 05:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nAsset', '0008_auto_20160415_0329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nasset',
            name='project_hub',
        ),
    ]