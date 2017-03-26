from django import forms
from pelanggan.models import Pelanggan

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
