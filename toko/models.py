from __future__ import unicode_literals
from pelanggan.models import Pelanggan
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Toko(models.Model):
    nama = models.CharField(max_length=32, db_index=True)
    # slug = models.SlugField(max_length=32, db_index=True)
    slogan = models.CharField(max_length=64)
    deskripsi = models.TextField(blank=True)
    alamat = models.CharField(max_length=32)
    pelanggan_id = models.ForeignKey(Pelanggan, related_name='pelanggant')

    def __unicode__(self):
        return self.nama

    def get_absolute_url(self):
        return reverse('toko:produk_list_by_toko', args=[self.id])

class Ratingtoko(models.Model):
    toko_id = models.ForeignKey(Toko, related_name='tokor')
    pelanggan_id = models.ForeignKey(Pelanggan, related_name='pelangganrt')
    ratingtoko = models.DecimalField(max_digits=10, decimal_places=2)
    komentar = models.TextField(blank=True)