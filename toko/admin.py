from django.contrib import admin
from .models import Toko, Ratingtoko

class TokoAdmin(admin.ModelAdmin):
    list_display = ['nama', 'slogan', 'deskripsi', 'alamat']
    # prepopulated_fields = {'slug': ('nama',)}
admin.site.register(Toko, TokoAdmin)

class RatingtokoAdmin(admin.ModelAdmin):
    list_display = ['toko_id', 'pelanggan_id', 'ratingtoko', 'komentar']
    list_filter = ['toko_id', 'pelanggan_id', 'ratingtoko', 'komentar']
admin.site.register(Ratingtoko, RatingtokoAdmin)