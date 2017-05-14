from __future__ import unicode_literals
from shop.models import Produk
from toko.models import Toko
from pelanggan.models import Pelanggan
from django.db import models

# Create your models here.
class Pesan(models.Model):
    waktu_pembelian = models.DateTimeField(auto_now_add=True)
    produk = models.ForeignKey(Produk)
    harga = models.PositiveIntegerField()
    kategori_harga = models.PositiveIntegerField()
    biaya_pengiriman = models.PositiveIntegerField()
    diskon = models.PositiveIntegerField()
    ratingproduk = models.PositiveIntegerField()
    ratingtoko = models.PositiveIntegerField()
    pelanggan = models.ForeignKey(Pelanggan)
    toko = models.ForeignKey(Toko)