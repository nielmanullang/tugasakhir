from django.contrib import admin

# Register your models here.
from .models import Pesanan

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ['produk']
#
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'nama', 'email', 'alamat', 'kodepos', 'kabupaten', 'paid', 'created', 'updated']
#     list_filter = ['paid', 'created', 'updated']
#     inlines = [OrderItemInline]
#
# admin.site.register(Order, OrderAdmin)

class PesananAdmin(admin.ModelAdmin):
    list_display = ['waktu_pembelian', 'harga', 'kategori_harga', 'biaya_pengiriman', 'diskon', 'ratingproduk', 'ratingtoko', 'pelanggan', 'toko']
    list_filter = ['waktu_pembelian', 'harga', 'kategori_harga', 'biaya_pengiriman', 'diskon', 'ratingproduk', 'ratingtoko', 'pelanggan', 'toko']
admin.site.register(Pesanan, PesananAdmin)