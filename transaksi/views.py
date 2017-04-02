from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from .forms import OrderTransaksiForm
from django.contrib.auth.models import User
from pelanggan.models import Pelanggan
from transaksi.models import Order
from transaksi.models import Transaksi
from shop.models import Produk
from django.shortcuts import render, get_object_or_404


def beli(request, produk_id, pelanggan_id):
    if request.method == 'POST':
        pelanggans = Pelanggan.objects.get(user_id=pelanggan_id)
        produks = Produk.objects.get(id=produk_id)
        hargaakhir = produks.harga - (produks.harga * produks.diskon / 100)
        transaksi = Transaksi.objects.create(
            produk_id=produks.id,
            harga=hargaakhir,
            kategori_harga='murah',
            biaya_pengiriman=20,
            pelanggan_id=pelanggans.id,
            toko=produks.toko_id
        )
    return render(request, 'transaksi/order/created.html')


def pembelian(request):
    if request.user.is_authenticated():
        current_user = request.user
        pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        pembelian = Transaksi.objects.filter(pelanggan_id=pelanggan.id)
        return render(request, 'transaksi/pembelian.html', {'pembelian': pembelian})
