# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-15 03:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nProject', '0004_auto_20160307_0514'),
    ]

    operations = [
        migrations.AddField(
            model_name='nprojecthub',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nProject.nProject'),
        ),
        migrations.AddField(
            model_name='nprojectpart',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nProject.nProject'),
        ),
    ]
