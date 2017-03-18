from django.contrib import admin
from pelanggan.models import *

# Register your models here.

class PelangganAdmin (admin.ModelAdmin):
    list_display = ['nama', 'no_telepon', 'jenis_kelamin', 'kabupaten', 'alamat', 'kodepos' ]
    list_filter = ('jenis_kelamin', 'kabupaten')
    search_fields = ['nama', 'alamat', 'email', 'no_telepon']
    list_per_page = 25

admin.site.register(Pelanggan, PelangganAdmin)

class AkunAdmin(admin.ModelAdmin):
    list_display = ['akun', 'pelanggan', 'jenis_akun']
    list_filter = ('jenis_akun',)
    search_fields = []
    list_per_page = 25

admin.site.register(Akun, AkunAdmin)