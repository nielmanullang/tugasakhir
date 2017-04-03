from django.contrib import admin
from .models import Ongkoskirim

# Register your models here.

class OngkosKirimAdmin(admin.ModelAdmin):
    list_display = ['kabupaten_asal', 'kabupaten_tujuan', 'biaya']
    list_filter = ['kabupaten_asal', 'kabupaten_tujuan', 'biaya']
admin.site.register(Ongkoskirim, OngkosKirimAdmin)