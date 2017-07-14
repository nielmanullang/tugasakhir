from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Pohonkeputusan(models.Model):
    waktu_transaksi = models.DateTimeField(auto_now=True, null=True)
    kategoriharga = models.PositiveIntegerField()
    ongkoskirim = models.PositiveIntegerField()
    diskon = models.PositiveIntegerField()
    ratingproduk = models.PositiveIntegerField()
    ratingtoko = models.PositiveIntegerField()
    label = models.PositiveIntegerField()
    pelanggan = models.PositiveIntegerField()
    perdaerah = models.CharField(max_length=32, null=True)

    # def save(self):
    #     if self.id:
    #         self.modified_date = datetime.now()
    #     else:
    #         self.created_date = datetime.now()
    #     super(Pohonkeputusan, self).save()