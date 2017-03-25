from django import forms
from . models import Pelanggan
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class CreatePelangganForm(forms.ModelForm):
    class Meta:
        model = Pelanggan
        fields = [
            'nama',
            'no_telepon',
            'jenis_kelamin',
            'kabupaten',
            'alamat',
            'kodepos',
        ]
