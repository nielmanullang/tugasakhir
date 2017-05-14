# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-13 05:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pelanggan', '0006_auto_20170504_2027'),
        ('toko', '0001_initial'),
        ('shop', '0003_auto_20170510_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pesan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_pembelian', models.DateTimeField(auto_now_add=True)),
                ('harga', models.DecimalField(decimal_places=0, max_digits=10)),
                ('kategori_harga', models.DecimalField(decimal_places=0, max_digits=1)),
                ('biaya_pengiriman', models.DecimalField(decimal_places=0, max_digits=10)),
                ('diskon', models.DecimalField(decimal_places=0, max_digits=1)),
                ('ratingproduk', models.DecimalField(decimal_places=0, max_digits=1)),
                ('ratingtoko', models.DecimalField(decimal_places=0, max_digits=1)),
                ('pelanggan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pelanggan.Pelanggan')),
                ('produk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Produk')),
                ('toko', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toko.Toko')),
            ],
        ),
    ]
