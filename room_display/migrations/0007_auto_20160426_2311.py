# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_display', '0006_auto_20160425_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='email',
            field=models.EmailField(default='abc@mail.mcgill.ca', max_length=254),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
