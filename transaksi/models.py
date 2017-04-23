from __future__ import unicode_literals
from shop.models import Produk
from toko.models import Toko
from pelanggan.models import Pelanggan
from django.db import models

class Transaksi(models.Model):
    waktu_pembelian = models.DateTimeField(auto_now_add=True)
    produk = models.ForeignKey(Produk, related_name='pesanan_produks')
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kategori_harga = models.CharField(max_length=5)
    biaya_pengiriman = models.DecimalField(max_digits=10, decimal_places=2)
    diskon = models.DecimalField(max_digits=2, decimal_places=0)
    ratingproduk = models.DecimalField(max_digits=2, decimal_places=0)
    ratingtoko = models.DecimalField(max_digits=2, decimal_places=0)
    pelanggan = models.ForeignKey(Pelanggan, related_name='pesanan_pelanggans')
    toko = models.ForeignKey(Toko, related_name='pesanan_tokos')

    # def __unicode__(self):
    #     return self.produk

    # def __str__(self):
    #     return self.waktu_pembelian