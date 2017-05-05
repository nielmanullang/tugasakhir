from django.contrib import admin
from .models import Kategori, Produk, Ratingproduk

class KategoriAdmin(admin.ModelAdmin):
    list_display = ['nama']
admin.site.register(Kategori, KategoriAdmin)

class ProdukAdmin(admin.ModelAdmin):
    list_display = ['nama', 'kategori', 'harga', 'stok', 'diskon', 'available']
    list_filter = ['available', 'kategori', 'diskon']
    # list_editable = ['harga', 'stok', 'available']
admin.site.register(Produk, ProdukAdmin)

class RatingprodukAdmin(admin.ModelAdmin):
    list_display = ['produk_id', 'pelanggan_id', 'ratingproduk', 'komentar']
    list_filter = ['produk_id', 'pelanggan_id', 'ratingproduk', 'komentar']
admin.site.register(Ratingproduk, RatingprodukAdmin)