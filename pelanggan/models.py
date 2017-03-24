from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pelanggan(models.Model):
    JENIS_KELAMIN_CHOICES = (
        ('pria', 'Pria'),
        ('wanita', 'Wanita'),
    )

    KABUPATEN_CHOICES = (
        ('KabupatenAsahan', 'Kabupaten Asahan'),
        ('kabupatenBatubara', 'Kabupaten Batubara'),
        ('KabupatenDairi', 'Kabupaten Dairi'),
        ('KabupatenDeliSerdang', 'Kabupaten Deli Serdang'),
        ('KabupatenHumbangHasudutan', 'Kabupaten Humbang Hasudutan'),
        ('KabupatenKaro', 'Kabupaten Karo'),
        ('KabupatenLabuhanBatu', 'Kabupaten Labuhan Batu'),
        ('KabupatenLabuhanBatuSelatan', 'Kabupaten Labuhan Batu Selatan'),
        ('KabupatenLabuhanBatuUtara', 'Kabupaten Labuhan Batu Utara'),
        ('KabupatenHumbangLangkat', 'Kabupaten Humbang Langkat'),
        ('KabupatenMandailingNatal', 'Kabupaten Mandailing Natal'),
        ('KabupatenNias', 'Kabupaten Nias'),
        ('KabupatenNiasBarat', 'Kabupaten Nias Barat'),
        ('KabupatenNiasSelatan', 'Kabupaten Nias Selatan'),
        ('KabupatenNiasUtara', 'Kabupaten Nias Utara'),
        ('KabupatenPadangLawas', 'Kabupaten Padang Lawas'),
        ('KabupatenPadangLawasUtara', 'Kabupaten Padang Lawas Utara'),
        ('KabupatenPakpakBharat', 'Kabupaten Pakpak Bharat'),
        ('KabupatenSamosir', 'Kabupaten Samosir'),
        ('KabupatenSerdangBedagai', 'Kabupaten Serdang Bedagai'),
        ('KabupatenTapanuli', 'Kabupaten Tapanuli'),
        ('kabupatenTapanuliSelatan', 'Kabupaten Tapanuli Selatan'),
        ('KabupatenTapanuliTengah', 'Kabupaten Tapanuli Tengah'),
        ('KabupatenTapanuliUtara', 'Kabupaten Tapanuli Utara'),
        ('KotaBinjai', 'Kota Binjai'),
        ('KotaGunungSitoli', 'Kota Gunung Sitoli'),
        ('KotaMedan', 'Kota Medan'),
        ('KotaPadangSidempuan', 'Kota Padang Sidempuan'),
        ('KotaPematangSiantar', 'Kota Pematang Siantar'),
        ('KotaSibolga', 'Kota Sibolga'),
        ('KotaTanjungBalai', 'Kota Tanjung Balai'),
        ('KotaTebingTinggi', 'Kota Tebing Tinggi'),
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