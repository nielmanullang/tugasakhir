from django import forms
from shop.models import Produk
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class CreatePrudukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = [
            'kategori',
            'nama',
            'gambar',
            'deskripsi',
            'harga',
            'stok',
            'available',
            'diskon',
        ]