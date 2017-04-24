from django.shortcuts import render
from django.contrib.auth.models import User
from pelanggan.models import Pelanggan
from pesanan.models import Pesanan
from referensiongkir.models import Ongkoskirim
from shop.models import Produk, Ratingproduk
from toko.models import Toko, Ratingtoko
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from pohonkeputusan.models import Pohonkeputusan

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
        if ratingproduk > 3:
            nilairatingproduk = 1
        else:
            nilairatingproduk = 0
        ratingtokos = Ratingtoko.objects.all().filter(toko_id=toko.id).aggregate(sum=Sum('ratingtoko'))['sum']
        counts = Ratingtoko.objects.all().filter(toko_id=toko.id).count()
        if counts == 0:
            ratingtoko = 0
        else:
            ratingtoko = ratingtokos / counts
        if ratingtoko > 3:
            nilairatingtoko = 1
        else:
            nilairatingtoko = 0
        if produks.diskon > 0:
            nilaidiskon = 1
        else:
            nilaidiskon = 0
        ongkoskirim = Ongkoskirim.objects.get(kabupaten_asal=pelanggans.kabupaten, kabupaten_tujuan=toko.alamat)
        if ongkoskirim.biaya > 0:
            nilaiongkoskirim = 0
        else:
            nilaiongkoskirim = 1
        kategoriharga = 10000
        if kategoriharga > 10000:
            nilaikategoriharga = 0
        else:
            nilaikategoriharga = 1
        pesanan = Pesanan.objects.create(produk_id=produks.id,
                                         harga=hargaakhir,
                                         kategori_harga=nilaikategoriharga,
                                         biaya_pengiriman=ongkoskirim.biaya,
                                         diskon=produks.diskon,
                                         ratingproduk=nilairatingproduk,
                                         ratingtoko=nilairatingtoko,
                                         pelanggan_id=pelanggans.id,
                                         toko=produks.toko_id)
        pesanan.save()
        pohonkeputusan = Pohonkeputusan.objects.create(kategoriharga=nilaikategoriharga,
                                                      ongkoskirim=nilaiongkoskirim,
                                                      diskon=nilaidiskon,
                                                      ratingproduk=nilairatingproduk,
                                                      ratingtoko=nilairatingtoko,
                                                      label=1,
                                                      pelanggan=pelanggans.id)
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
