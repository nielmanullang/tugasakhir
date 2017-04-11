# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 01:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pelanggan', '0001_initial'),
        ('toko', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(db_index=True, max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(db_index=True, max_length=200)),
                ('gambar', models.ImageField(blank=True, upload_to=b'produk')),
                ('deskripsi', models.TextField(blank=True)),
                ('harga', models.DecimalField(decimal_places=0, max_digits=10)),
                ('diskon', models.DecimalField(decimal_places=0, max_digits=2)),
                ('stok', models.PositiveIntegerField()),
                ('available', models.BooleanField(default=True)),
                ('kategori', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produks', to='shop.Kategori')),
                ('toko_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tokopr', to='toko.Toko')),
            ],
        ),
        migrations.CreateModel(
            name='Ratingproduk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratingproduk', models.DecimalField(decimal_places=0, max_digits=2)),
                ('komentar', models.TextField(blank=True)),
                ('pelanggan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pelangganr', to='pelanggan.Pelanggan')),
                ('produk_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produkr', to='shop.Produk')),
            ],
        ),
    ]
