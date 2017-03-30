from __future__ import unicode_literals
from shop.models import Produk
from toko.models import Toko
from pelanggan.models import Pelanggan
from django.db import models

# Create your models here.
class Order(models.Model):
    nama = models.CharField(max_length=50)
    email = models.EmailField()
    alamat = models.CharField(max_length=250)
    kodepos = models.CharField(max_length=20)
    kabupaten = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    produk = models.ForeignKey(Produk, related_name='order_items')
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    jumlah = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.harga * self.jumlah

class Transaksi(models.Model):
    waktu_pembelian = models.DateTimeField(auto_now_add=True)
    produk = models.ForeignKey(Produk, related_name='transaksi_produks')
    biaya_pengiriman = models.DecimalField(max_digits=10, decimal_places=2)
    pelanggan = models.ForeignKey(Pelanggan, related_name='transaksi_pelanggans')
    toko = models.ForeignKey(Toko, related_name='transaksi_tokos')

    def __unicode__(self):
        return self.waktu_pembelian