# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-24 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KimeoApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Light',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turnOn', models.BooleanField()),
                ('blink', models.BooleanField()),
                ('repeat', models.IntegerField()),
                ('intervalBlinking', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageName', models.CharField(max_length=100)),
                ('stay', models.BooleanField()),
                ('timeToStay', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soundName', models.CharField(max_length=100)),
                ('repeat', models.IntegerField()),
            ],
        ),
    ]
