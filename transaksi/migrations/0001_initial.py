# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-22 15:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('toko', '0001_initial'),
        ('pelanggan', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaksi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_pembelian', models.DateTimeField(auto_now_add=True)),
                ('harga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('kategori_harga', models.CharField(max_length=5)),
                ('biaya_pengiriman', models.DecimalField(decimal_places=2, max_digits=10)),
                ('diskon', models.DecimalField(decimal_places=0, max_digits=2)),
                ('ratingproduk', models.DecimalField(decimal_places=0, max_digits=2)),
                ('ratingtoko', models.DecimalField(decimal_places=0, max_digits=2)),
                ('pelanggan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaksi_pelanggans', to='pelanggan.Pelanggan')),
                ('produk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaksi_produks', to='shop.Produk')),
                ('toko', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaksi_tokos', to='toko.Toko')),
            ],
        ),
    ]
