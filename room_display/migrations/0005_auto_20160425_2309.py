# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 03:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('room_display', '0004_auto_20160425_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 26, 3, 9, 56, 11646, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='booking',
            name='date_stop',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 26, 3, 9, 56, 11795, tzinfo=utc)),
        ),
    ]
