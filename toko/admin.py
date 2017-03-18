from django.contrib import admin
from .models import Toko

class TokoAdmin(admin.ModelAdmin):
    list_display = ['nama', 'slug', 'slogan', 'deskripsi', 'alamat']
    prepopulated_fields = {'slug': ('nama',)}
admin.site.register(Toko, TokoAdmin)
