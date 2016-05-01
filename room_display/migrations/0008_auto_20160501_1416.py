# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 18:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_display', '0007_auto_20160426_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='classroom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='room_display.Classroom'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='number_seats',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='randomuser',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='room_display.Booking'),
        ),
    ]