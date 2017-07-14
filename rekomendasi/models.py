from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Rekomendasi(models.Model):
    produk_id = models.PositiveIntegerField()
    produk_nama = models.CharField(max_length=200, db_index=True)
    produk_gambar = models.CharField(max_length=200, db_index=True)
    produk_harga = models.DecimalField(max_digits=10, decimal_places=0)
    produk_diskon = models.DecimalField(max_digits=2, decimal_places=0)
    n_harga = models.PositiveIntegerField()
    n_ongkir = models.PositiveIntegerField()
    n_diskon = models.PositiveIntegerField()
    n_ratingproduk =  models.PositiveIntegerField()
    n_ratingtoko =  models.PositiveIntegerField()
    prediksi = models.PositiveIntegerField()