# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-17 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pohonkeputusan', '0005_auto_20170620_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pohonkeputusan',
            name='waktu_transaksi',
            field=models.DateTimeField(null=True),
        ),
    ]