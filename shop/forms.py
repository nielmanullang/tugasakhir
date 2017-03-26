from django import forms
from shop.models import Produk

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