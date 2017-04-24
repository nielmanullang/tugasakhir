from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Pohonkeputusan(models.Model):
    kategoriharga = models.PositiveIntegerField()
    ongkoskirim = models.PositiveIntegerField()
    diskon = models.PositiveIntegerField()
    ratingproduk = models.PositiveIntegerField()
    ratingtoko = models.PositiveIntegerField()
    label = models.PositiveIntegerField()
    pelanggan = models.PositiveIntegerField()