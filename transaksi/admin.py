from django.contrib import admin
from .models import Order, OrderItem
from .models import Transaksi

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

class TransaksiAdmin(admin.ModelAdmin):
    list_display = ['produk', 'waktu_pembelian', 'harga', 'biaya_pengiriman', 'pelanggan', 'toko']
    list_filter = ['waktu_pembelian', 'produk', 'pelanggan', 'toko']
admin.site.register(Transaksi, TransaksiAdmin)