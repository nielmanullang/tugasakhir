from django import forms
from .models import Order
from .models import Transaksi


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'nama',
            # 'email',
            # 'alamat',
            # 'kabupaten',
            # 'kodepos',
        ]

class OrderTransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = [
            'produk',
            'biaya_pengiriman',
            'pelanggan',
            'toko',
        ]