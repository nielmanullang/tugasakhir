from django.contrib import admin
from .models import Kategori, Produk

class KategoriAdmin(admin.ModelAdmin):
    list_display = ['nama', 'slug']
    prepopulated_fields = {'slug': ('nama',)}
admin.site.register(Kategori, KategoriAdmin)

class ProdukAdmin(admin.ModelAdmin):
    list_display = ['nama', 'slug', 'kategori', 'harga', 'stok', 'available']
    list_filter = ['available', 'kategori']
    list_editable = ['harga', 'stok', 'available']
    prepopulated_fields = {'slug': ('nama',)}
admin.site.register(Produk, ProdukAdmin)