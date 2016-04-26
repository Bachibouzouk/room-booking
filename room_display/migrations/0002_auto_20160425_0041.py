# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 04:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_display', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='date',
            name='booked_classrooms',
        ),
        migrations.AlterField(
            model_name='classroom',
            name='booked_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_display.Date'),
        ),
        migrations.AddField(
            model_name='booking',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_display.Classroom'),
        ),
    ]
