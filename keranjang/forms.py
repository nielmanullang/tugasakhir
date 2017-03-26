from django import forms
PILIHAN_JUMLAH_PRODUK = [(i, str(i)) for i in range(1, 21)]

class KeranjangTambahProdukForm(forms.Form):
    jumlah = forms.TypedChoiceField(choices=PILIHAN_JUMLAH_PRODUK, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
