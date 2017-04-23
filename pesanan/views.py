from django.shortcuts import render
from django.contrib.auth.models import User
from pelanggan.models import Pelanggan
from pesanan.models import Pesanan
from referensiongkir.models import Ongkoskirim
from shop.models import Produk, Ratingproduk
from toko.models import Toko, Ratingtoko
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum


def beli(request, produk_id, pelanggan_id):
    if request.method == 'POST':
        pelanggans = Pelanggan.objects.get(user_id=pelanggan_id)
        produks = Produk.objects.get(id=produk_id)
        toko = Toko.objects.get(id=produks.toko_id_id)
        hargaakhir = produks.harga - (produks.harga * produks.diskon / 100)
        ratingproduks = Ratingproduk.objects.all().filter(produk_id=produk_id).aggregate(sum=Sum('ratingproduk'))['sum']
        count = Ratingproduk.objects.all().filter(produk_id=produk_id).count()
        if count == 0:
            ratingproduk = 0
        else:
            ratingproduk = ratingproduks / count
        ratingtokos = Ratingtoko.objects.all().filter(toko_id=toko.id).aggregate(sum=Sum('ratingtoko'))['sum']
        counts = Ratingtoko.objects.all().filter(toko_id=toko.id).count()
        if counts == 0:
            ratingtoko = 0
        else:
            ratingtoko = ratingtokos / counts
        ongkoskirim = Ongkoskirim.objects.get(kabupaten_asal=pelanggans.kabupaten, kabupaten_tujuan=toko.alamat)
        pesanan = Pesanan.objects.create(
            produk_id=produks.id,
            harga=hargaakhir,
            kategori_harga='murah',
            biaya_pengiriman=ongkoskirim.biaya,
            diskon=produks.diskon,
            ratingproduk=ratingproduk,
            ratingtoko=ratingtoko,
            pelanggan_id=pelanggans.id,
            toko=produks.toko_id
        )
    return render(request, 'pesanan/order/created.html')


def pembelian(request):
    current_user = request.user
    if (current_user is not None):
        try:
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        except Pelanggan.DoesNotExist:
            pelanggan = None
        if (pelanggan is not None):
            pembelian = Pesanan.objects.filter(pelanggan_id=pelanggan.id)
            return render(request, 'pesanan/pembelian.html', {'pembelian': pembelian})
        else:
            return render(request, 'toko/toko_null.html')
    else:
        return render(request, 'toko/toko_null.html')


def penjualan(request):
    if request.user.is_authenticated():
        current_user = request.user
        pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        toko = Toko.objects.get(pelanggan_id=pelanggan.id)
        penjualan = Pesanan.objects.filter(toko_id=toko.id)
        return render(request, 'pesanan/penjualan.html', {'penjualan': penjualan})
