from django.contrib import admin
from .models import Pohonkeputusan
from datetime import datetime
# Register your models here.
class PohonkeputusanAdmin(admin.ModelAdmin):
    list_display = ['waktu_transaksi','kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko', 'label', 'pelanggan', 'perdaerah']
    list_filter = ['waktu_transaksi','kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko', 'label', 'pelanggan', 'perdaerah']
    def save_model(self, request, obj, form, change):
        if obj.label and 'label' in form.changed_data:
            obj.waktu_transaksi = datetime.now()
            obj.save()
admin.site.register(Pohonkeputusan, PohonkeputusanAdmin)