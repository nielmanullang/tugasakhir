from django.shortcuts import render
from django.contrib.auth.models import User
from pelanggan.models import Pelanggan
from pesanan.models import Pesanan
from referensiongkir.models import Ongkoskirim
from shop.models import Produk, Ratingproduk, Kategori
from toko.models import Toko, Ratingtoko
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from pohonkeputusan.models import Pohonkeputusan
import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd
from sklearn.cluster import KMeans
from django_pandas.io import read_frame


def beli(request, produk_id, pelanggan_id):
    current_user = request.user
    if (current_user is not None):
        try:
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        except Pelanggan.DoesNotExist:
            pelanggan = None
        if (pelanggan is not None):
            if request.method == 'POST':
                pelanggans = Pelanggan.objects.get(user_id=pelanggan_id)
                produks = Produk.objects.get(id=produk_id)
                toko = Toko.objects.get(id=produks.toko_id_id)
                hargaakhir = produks.harga - (produks.harga * produks.diskon / 100)
                ratingproduks = \
                Ratingproduk.objects.all().filter(produk_id=produk_id).aggregate(sum=Sum('ratingproduk'))['sum']
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

                # pesanan = Pesanan.objects.filter(pelanggan_id=pelanggan.id).order_by('-id')[0]
                produk = Produk.objects.get(id=produk_id)
                kategori = Produk.objects.all().filter(kategori_id=produk.kategori)
                # kmeans
                # Importing the dataset untuk harga
                dff = read_frame(kategori,
                                 fieldnames=['nama', 'gambar', 'deskripsi', 'harga', 'diskon', 'stok', 'available'])
                Z = dff.iloc[:, [4]].values
                # Fitting K-Means to the dataset
                kmeans = KMeans(n_clusters=2, init='k-means++', random_state=42)
                y_kmeans = kmeans.fit_predict(Z)

                pesanan = Pesanan.objects.create(produk_id=produks.id,
                                                 harga=hargaakhir,
                                                 kategori_harga=y_kmeans[0],
                                                 biaya_pengiriman=ongkoskirim.biaya,
                                                 diskon=produks.diskon,
                                                 ratingproduk=nilairatingproduk,
                                                 ratingtoko=nilairatingtoko,
                                                 pelanggan_id=pelanggans.id,
                                                 toko=produks.toko_id)
                pesanan.save()
                pohonkeputusan = Pohonkeputusan.objects.create(kategoriharga=y_kmeans[0],
                                                               ongkoskirim=nilaiongkoskirim,
                                                               diskon=nilaidiskon,
                                                               ratingproduk=nilairatingproduk,
                                                               ratingtoko=nilairatingtoko,
                                                               label=1,
                                                               pelanggan=pelanggans.id)
                pohonkeputusan.save()
            return render(request, 'pesanan/order/created.html')
        else:
            return render(request, 'pesanan/pelanggan_null.html')
    else:
        return render(request, 'pesanan/pelanggan_null.html')


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
