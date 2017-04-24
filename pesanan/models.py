from __future__ import unicode_literals
from shop.models import Produk
from toko.models import Toko
from pelanggan.models import Pelanggan
from django.db import models

# Create your models here.
class Pesanan(models.Model):
    waktu_pembelian = models.DateTimeField(auto_now_add=True)
    produk = models.ForeignKey(Produk, related_name='transaksi_produks')
    harga = models.DecimalField(max_digits=10, decimal_places=0)
    kategori_harga = models.DecimalField(max_digits=1, decimal_places=0)
    biaya_pengiriman = models.DecimalField(max_digits=10, decimal_places=0)
    diskon = models.DecimalField(max_digits=1, decimal_places=0)
    ratingproduk = models.DecimalField(max_digits=1, decimal_places=0)
    ratingtoko = models.DecimalField(max_digits=1, decimal_places=0)
    pelanggan = models.ForeignKey(Pelanggan, related_name='transaksi_pelanggans')
    toko = models.ForeignKey(Toko, related_name='transaksi_tokos')