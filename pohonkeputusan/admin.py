from django.contrib import admin
from .models import Pohonkeputusan

# Register your models here.
class PohonkeputusanAdmin(admin.ModelAdmin):
    list_display = ['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko', 'label', 'pelanggan']
    list_filter = ['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko', 'label', 'pelanggan']
admin.site.register(Pohonkeputusan, PohonkeputusanAdmin)