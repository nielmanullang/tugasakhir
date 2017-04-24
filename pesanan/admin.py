from django.contrib import admin

# Register your models here.
from .models import Pesanan


class PesananAdmin(admin.ModelAdmin):
    list_display = ['waktu_pembelian', 'harga', 'kategori_harga', 'biaya_pengiriman', 'diskon', 'ratingproduk',
                    'ratingtoko', 'pelanggan', 'toko']
    list_filter = ['waktu_pembelian', 'harga', 'kategori_harga', 'biaya_pengiriman', 'diskon', 'ratingproduk',
                   'ratingtoko', 'pelanggan', 'toko']


admin.site.register(Pesanan, PesananAdmin)
