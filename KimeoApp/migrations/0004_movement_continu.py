# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-15 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KimeoApp', '0003_movement_headposition'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='continu',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]