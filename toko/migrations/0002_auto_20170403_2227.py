# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toko', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingtoko',
            name='ratingtoko',
            field=models.DecimalField(decimal_places=0, max_digits=2),
        ),
    ]
