from django.db import models
from django.core.urlresolvers import reverse
from pelanggan.models import Pelanggan
from toko.models import Toko

JENIS_DISKON_CHOICES = (
    ('tidakada', 'Tidak Ada'),
    ('Ada', 'Ada'),
)

class Kategori(models.Model):
    nama = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.nama

    def get_absolute_url(self):
        return reverse('shop:produk_list_by_kategori', args=[self.slug])

class Produk(models.Model):
    kategori = models.ForeignKey(Kategori, related_name='produks')
    nama = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    gambar = models.ImageField(upload_to='produk', blank=True)
    deskripsi = models.TextField(blank=True)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    diskon = models.CharField(max_length=10, choices=JENIS_DISKON_CHOICES)
    toko_id = models.ForeignKey(Toko, on_delete=models.CASCADE, null=True, related_name='tokopr')

    def __str__(self):
        return self.nama

    def get_absolute_url(self):
        return reverse('shop:produk_detail', args=[self.id, self.slug])

class Ratingproduk(models.Model):
    produk_id = models.ForeignKey(Produk, related_name='produkr')
    pelanggan_id = models.ForeignKey(Pelanggan, related_name='pelangganr')
    ratingproduk = models.DecimalField(max_digits=10, decimal_places=2)
    komentar = models.TextField(blank=True)