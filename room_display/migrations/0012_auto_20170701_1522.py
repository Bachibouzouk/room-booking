# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-01 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_display', '0011_auto_20170528_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='key',
            field=models.CharField(default='5dea1ebb3bf448d885e1cccd2b7f502b', max_length=32),
        ),
    ]
