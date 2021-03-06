from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Ongkoskirim(models.Model):
    KABUPATEN_CHOICES = (
        ('Kabupaten Asahan', 'Kabupaten Asahan'),
        ('Kabupaten Batubara', 'Kabupaten Batubara'),
        ('Kabupaten Dairi', 'Kabupaten Dairi'),
        ('Kabupaten Deli Serdang', 'Kabupaten Deli Serdang'),
        ('Kabupaten Humbang Hasudutan', 'Kabupaten Humbang Hasudutan'),
        ('Kabupaten Karo', 'Kabupaten Karo'),
        ('Kabupaten Labuhan Batu', 'Kabupaten Labuhan Batu'),
        ('Kabupaten Labuhan Batu Selatan', 'Kabupaten Labuhan Batu Selatan'),
        ('Kabupaten Labuhan Batu Utara', 'Kabupaten Labuhan Batu Utara'),
        ('Kabupaten Langkat', 'Kabupaten Langkat'),
        ('Kabupaten Mandailing Natal', 'Kabupaten Mandailing Natal'),
        ('Kabupaten Nias', 'Kabupaten Nias'),
        ('Kabupaten Nias Barat', 'Kabupaten Nias Barat'),
        ('Kabupaten Nias Selatan', 'Kabupaten Nias Selatan'),
        ('Kabupaten Nias Utara', 'Kabupaten Nias Utara'),
        ('Kabupaten Padang Lawas', 'Kabupaten Padang Lawas'),
        ('Kabupaten Padang Lawas Utara', 'Kabupaten Padang Lawas Utara'),
        ('Kabupaten Pakpak Bharat', 'Kabupaten Pakpak Bharat'),
        ('Kabupaten Samosir', 'Kabupaten Samosir'),
        ('Kabupaten Serdang Bedagai', 'Kabupaten Serdang Bedagai'),
        ('Kabupaten Simalungun', 'Kabupaten Simalungun'),
        ('Kabupaten Tapanuli Selatan', 'Kabupaten Tapanuli Selatan'),
        ('Kabupaten Tapanuli Tengah', 'Kabupaten Tapanuli Tengah'),
        ('Kabupaten Tapanuli Utara', 'Kabupaten Tapanuli Utara'),
        ('Kabupaten Toba Samosir', 'Kabupaten Toba Samosir'),
        ('Kota Binjai', 'Kota Binjai'),
        ('Kota Gunung Sitoli', 'Kota Gunung Sitoli'),
        ('Kota Medan', 'Kota Medan'),
        ('Kota Padang Sidempuan', 'Kota Padang Sidempuan'),
        ('Kota Pematang Siantar', 'Kota Pematang Siantar'),
        ('Kota Sibolga', 'Kota Sibolga'),
        ('Kota Tanjung Balai', 'Kota Tanjung Balai'),
        ('Kota Tebing Tinggi', 'Kota Tebing Tinggi'),
    )

    kabupaten_asal = models.CharField(max_length=32, choices=KABUPATEN_CHOICES)
    kabupaten_tujuan = models.CharField(max_length=32, choices=KABUPATEN_CHOICES)
    biaya = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.kabupaten_asal