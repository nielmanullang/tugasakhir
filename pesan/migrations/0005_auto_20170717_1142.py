# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-17 04:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesan', '0004_auto_20170717_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesan',
            name='waktu_pembelian',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
