from django.shortcuts import render
from django.contrib.auth.models import User
from pelanggan.models import Pelanggan
from pesan.models import Pesan
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
import itertools
from datetime import datetime
from django.utils import timezone

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

                ratingproduks = Ratingproduk.objects.all().filter(produk_id=produk_id).aggregate(sum=Sum('ratingproduk'))['sum']
                count = Ratingproduk.objects.all().filter(produk_id=produk_id).count()
                if count == 0:
                    ratingproduk = 0
                else:
                    ratingproduk = ratingproduks / count
                if ratingproduk == 0:
                    nilairatingproduk = 0
                elif ratingproduk == 1:
                    nilairatingproduk = 1
                elif ratingproduk == 2:
                    nilairatingproduk = 2
                elif ratingproduk == 3:
                    nilairatingproduk = 3
                elif ratingproduk == 4:
                    nilairatingproduk = 4
                elif ratingproduk == 5:
                    nilairatingproduk = 5

                ratingtokos = Ratingtoko.objects.all().filter(toko_id=toko.id).aggregate(sum=Sum('ratingtoko'))['sum']
                counts = Ratingtoko.objects.all().filter(toko_id=toko.id).count()
                if counts == 0:
                    ratingtoko = 0
                else:
                    ratingtoko = ratingtokos / counts
                if ratingtoko == 0:
                    nilairatingtoko = 0
                elif ratingtoko == 1:
                    nilairatingtoko = 1
                elif ratingtoko == 2:
                    nilairatingtoko = 2
                elif ratingtoko == 3:
                    nilairatingtoko = 3
                elif ratingtoko == 4:
                    nilairatingtoko = 4
                elif ratingtoko == 5:
                    nilairatingtoko = 5

                if produks.diskon > 0:
                    nilaidiskon = 1
                else:
                    nilaidiskon = 0
                ongkoskirim = Ongkoskirim.objects.get(kabupaten_asal=pelanggans.kabupaten, kabupaten_tujuan=toko.alamat)
                if ongkoskirim.biaya > 0:
                    nilaiongkoskirim = 0
                else:
                    nilaiongkoskirim = 1

                pesan = Pesan.objects.create(produk_id=produks.id,
                                             harga=hargaakhir,
                                             kategori_harga=produks.kmeansharga,
                                             biaya_pengiriman=ongkoskirim.biaya,
                                             diskon=produks.diskon,
                                             ratingproduk=nilairatingproduk,
                                             ratingtoko=nilairatingtoko,
                                             pelanggan_id=pelanggans.id,
                                             toko=produks.toko_id)
                pesan.save()
                countdata = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id).count()
                belanjasaya = str(produks.kmeansharga) + str(nilaiongkoskirim) + str(nilaidiskon) + str(nilairatingproduk) + str(nilairatingtoko)
                if (countdata == 0):
                    # kombinasi = ["".join(seq) for seq in itertools.product("01", repeat=5)]
                    kombinasi = ["".join(seq) for seq in itertools.product(["0","1"], ["0","1"], ["0","1"], ["0","1","2","3","4","5"], ["0","1","2","3","4","5"])]
                    for kom in kombinasi:
                        label = 0
                        if kom == belanjasaya:
                            label = 1
                        pohonkeputusan = Pohonkeputusan.objects.create(waktu_transaksi=datetime.now(),
                                                                       kategoriharga=kom[0],
                                                                       ongkoskirim=kom[1],
                                                                       diskon=kom[2],
                                                                       ratingproduk=kom[3],
                                                                       ratingtoko=kom[4],
                                                                       label=label,
                                                                       pelanggan=pelanggans.id,
                                                                       perdaerah=pelanggan.kabupaten)
                else:
                    pohonkeputusanupdate = Pohonkeputusan.objects.filter(kategoriharga=produks.kmeansharga,
                                                                         ongkoskirim=nilaiongkoskirim,
                                                                         diskon=nilaidiskon,
                                                                         ratingproduk=nilairatingproduk,
                                                                         ratingtoko=nilairatingtoko).update(label=1, waktu_transaksi=datetime.today())

            return render(request, 'pesan/order/created.html')
        else:
            return render(request, 'pesan/pelanggan_null.html')
    else:
        return render(request, 'pesan/pelanggan_null.html')


def pembelian(request):
    current_user = request.user
    if (current_user is not None):
        try:
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        except Pelanggan.DoesNotExist:
            pelanggan = None
        if (pelanggan is not None):
            pembelian = Pesan.objects.filter(pelanggan_id=pelanggan.id)
            return render(request, 'pesan/pembelian.html', {'pembelian': pembelian})
        else:
            return render(request, 'toko/toko_null.html')
    else:
        return render(request, 'toko/toko_null.html')


def penjualan(request):
    if request.user.is_authenticated():
        current_user = request.user
        pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        toko = Toko.objects.get(pelanggan_id=pelanggan.id)
        penjualan = Pesan.objects.filter(toko_id=toko.id)
        return render(request, 'pesan/penjualan.html', {'penjualan': penjualan})
