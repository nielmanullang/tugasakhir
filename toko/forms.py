from django import forms
from . models import Toko
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class CreateTokoForm(forms.ModelForm):
    class Meta:
        model = Toko
        fields = [
            'nama',
            'slogan',
            'deskripsi',
        ]
    # nama = forms.CharField(label='Nama', max_length=30)
    # slogan = forms.CharField(label='Slogan', max_length=100)
    # deskripsi = forms.CharField(label='Deskripsi', max_length=250)