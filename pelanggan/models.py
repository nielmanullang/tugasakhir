from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pelanggan(models.Model):
    JENIS_KELAMIN_CHOICES = (
        ('Pria', 'Pria'),
        ('Wanita', 'Wanita'),
    )

    KABUPATEN_CHOICES = (
        ('Kabupaten Asahan', 'Kabupaten Asahan'),
        ('kabupaten Batubara', 'Kabupaten Batubara'),
        ('Kabupaten Dairi', 'Kabupaten Dairi'),
        ('Kabupaten Deli Serdang', 'Kabupaten Deli Serdang'),
        ('Kabupaten Humbang Hasudutan', 'Kabupaten Humbang Hasudutan'),
        ('Kabupaten Karo', 'Kabupaten Karo'),
        ('Kabupaten Labuhan Batu', 'Kabupaten Labuhan Batu'),
        ('Kabupaten Labuhan Batu Selatan', 'Kabupaten Labuhan Batu Selatan'),
        ('Kabupaten Labuhan Batu Utara', 'Kabupaten Labuhan Batu Utara'),
        ('Kabupaten Humbang Langkat', 'Kabupaten Humbang Langkat'),
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
        ('Kabupaten Tapanuli', 'Kabupaten Tapanuli'),
        ('kabupaten Tapanuli Selatan', 'Kabupaten Tapanuli Selatan'),
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

    nama = models.CharField(max_length=100)
    no_telepon = models.CharField(max_length=30, blank=True)
    jenis_kelamin = models.CharField(max_length=10, choices=JENIS_KELAMIN_CHOICES)
    kabupaten = models.CharField(max_length=32, choices=KABUPATEN_CHOICES)
    alamat = models.TextField(blank=True)
    kodepos = models.CharField(max_length=5)
    user_id = models.ForeignKey(User, related_name='users')

    def __unicode__(self):
        return self.nama