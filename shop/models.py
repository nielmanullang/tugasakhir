from django.db import models
from django.core.urlresolvers import reverse
from pelanggan.models import Pelanggan
from toko.models import Toko


class Kategori(models.Model):
    nama = models.CharField(max_length=200, db_index=True, unique=True)

    # slug = models.SlugField(max_length=200, db_index=True)

    def __str__(self):
        return self.nama

    def get_absolute_url(self):
        return reverse('shop:produk_list_by_kategori', args=[self.id])


class Produk(models.Model):
    kategori = models.ForeignKey(Kategori, related_name='produks')
    nama = models.CharField(max_length=200, db_index=True)
    gambar = models.ImageField(upload_to='produk/', blank=True)
    deskripsi = models.TextField(blank=True)
    harga = models.DecimalField(max_digits=10, decimal_places=0)
    diskon = models.DecimalField(max_digits=2, decimal_places=0)
    stok = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    toko_id = models.ForeignKey(Toko, on_delete=models.CASCADE, null=True, related_name='tokopr')
    kmeansharga = models.PositiveIntegerField(null=True)
    kategoriongkoskirim = models.PositiveIntegerField(null=True)
    kategoridiskon = models.PositiveIntegerField(null=True)
    kategoriratingproduk = models.PositiveIntegerField(null=True)
    kategoriratingtoko = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.nama

    def get_absolute_url(self):
        return reverse('shop:produk_detail', args=[self.kategori_id, self.id])


class Ratingproduk(models.Model):
    produk_id = models.ForeignKey(Produk, related_name='produkr')
    pelanggan_id = models.ForeignKey(Pelanggan, related_name='pelangganr')
    ratingproduk = models.DecimalField(max_digits=2, decimal_places=0)
    komentar = models.TextField(blank=True)


class Rekomendasi(models.Model):
    produk_id = models.PositiveIntegerField()
    produk_kategori = models.PositiveIntegerField(null=True)
    produk_nama = models.CharField(max_length=200, db_index=True)
    produk_gambar = models.ImageField(upload_to='produk/', blank=True)
    produk_harga = models.DecimalField(max_digits=10, decimal_places=0)
    produk_diskon = models.DecimalField(max_digits=2, decimal_places=0)
    n_harga = models.PositiveIntegerField()
    n_ongkir = models.PositiveIntegerField()
    n_diskon = models.PositiveIntegerField()
    n_ratingproduk =  models.PositiveIntegerField()
    n_ratingtoko =  models.PositiveIntegerField()
    prediksi = models.PositiveIntegerField()
    pelanggan = models.PositiveIntegerField()

    def __str__(self):
        return self.produk_nama

    def get_absolute_url(self):
        return reverse('shop:produk_detail', args=[self.produk_kategori, self.produk_id])