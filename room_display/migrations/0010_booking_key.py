# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-29 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_display', '0009_booking_booking_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='key',
            field=models.CharField(default='6459fd4f83244d888891eb4eec03b0b1', max_length=32),
        ),
    ]
