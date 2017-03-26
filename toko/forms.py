from django import forms
from . models import Toko

class CreateTokoForm(forms.ModelForm):
    class Meta:
        model = Toko
        fields = [
            'nama',
            'slogan',
            'deskripsi',
        ]