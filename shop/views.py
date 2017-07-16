from django.shortcuts import render, get_object_or_404
from .models import Kategori, Produk, Ratingproduk, Rekomendasi
from .forms import CreatePrudukForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from pelanggan.models import Pelanggan
from toko.models import Toko, Ratingtoko
from referensiongkir.models import Ongkoskirim
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Sum
from pohonkeputusan.models import Pohonkeputusan
import psycopg2 as pg
import pandas.io.sql as psql
from sklearn.cluster import KMeans
from django_pandas.io import read_frame
import numpy as np
from django.db.models import Count


# @login_required(login_url=settings.LOGIN_URL)
def produk_list(request, kategori_id=None):
    kategori = None
    kategoris = Kategori.objects.all()
    produks = Produk.objects.filter(available=True)  # .order_by('-id')[:9:1]
    # untuk mengupdate kategori ongkos kirim berdasarkan yang login
    current_user = request.user
    rekomendasi = Rekomendasi.objects.filter(prediksi=1)
    if (current_user is not None):
        try:
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        except Pelanggan.DoesNotExist:
            pelanggan = None
        if (pelanggan is not None):
            rekomendasi = Rekomendasi.objects.filter(prediksi=1, pelanggan=pelanggan.id)
        else:
            rekomendasi = 'Belum ada rekomendasi untuk Anda'
    if (current_user is not None):
        try:
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        except Pelanggan.DoesNotExist:
            pelanggan = None
        if (pelanggan is not None):
            selectsemuaproduk = Produk.objects.all()
            for produs in selectsemuaproduk:
                toko = Toko.objects.get(id=produs.toko_id_id)
                biayakirim = Ongkoskirim.objects.get(kabupaten_asal=pelanggan.kabupaten, kabupaten_tujuan=toko.alamat)
                if biayakirim.biaya > 0:
                    produkupdate = Produk.objects.filter(id=produs.id).update(kategoriongkoskirim=0)
                else:
                    produkupdate = Produk.objects.filter(id=produs.id).update(kategoriongkoskirim=1)
    #untuk mengupdate kmeans harga
    selectsemuakategori = Kategori.objects.all()
    for kateg in selectsemuakategori:
        ketegori = Produk.objects.all().filter(kategori_id=kateg).order_by('id')
        dff = read_frame(ketegori, fieldnames=['nama', 'gambar', 'deskripsi', 'harga', 'diskon', 'stok', 'available'])
        Z = dff.iloc[:, [3]].values
        # Fitting K-Means to the dataset
        kmeans = KMeans(n_clusters=2, init='k-means++', random_state=42)
        kmeanshargasss = kmeans.fit_predict(Z)
        i = 0
        for k in ketegori:
            produk = Produk.objects.filter(id=k.id).update(kmeansharga=kmeanshargasss[i])
            i += 1
    # untuk mengupdate kategori rating toko
    ratingtokos = Ratingtoko.objects.all()
    for rts in ratingtokos:
        if rts.ratingtoko > 3:
            produkupdate = Produk.objects.filter(toko_id=rts.toko_id_id).update(kategoriratingtoko=1)
        else:
            produkupdate = Produk.objects.filter(toko_id=rts.toko_id_id).update(kategoriratingtoko=0)
    # untuk mengupdate kategori rating produk
    ratingproduks = Ratingproduk.objects.all()
    for rp in ratingproduks:
        if rp.ratingproduk > 3:
            produkupdate = Produk.objects.filter(id=rp.produk_id_id).update(kategoriratingproduk=1)
        else:
            produkupdate = Produk.objects.filter(id=rp.produk_id_id).update(kategoriratingproduk=0)
    # untuk mengupdate kategori rating diskon
    diskons = Produk.objects.all()
    for dk in diskons:
        if dk.diskon > 0:
            produkupdate = Produk.objects.filter(id=dk.id).update(kategoridiskon=1)
        else:
            produkupdate = Produk.objects.filter(id=dk.id).update(kategoridiskon=0)
    query = request.GET.get("search_produk")
    if query:
        produks = Produk.objects.filter(nama__icontains=query)
    if kategori_id:
        kategori = Produk.objects.all().filter(kategori_id=kategori_id).order_by('id')
        # # Importing the dataset untuk kmeans harga
        # dff = read_frame(kategori, fieldnames=['nama', 'gambar', 'deskripsi', 'harga', 'diskon', 'stok', 'available'])
        # Z = dff.iloc[:, [3]].values
        # # Fitting K-Means to the dataset
        # kmeans = KMeans(n_clusters=2, init='k-means++', random_state=42)
        # kmeanshargasss = kmeans.fit_predict(Z)
        # i = 0
        # for k in kategori:
        #     produk = Produk.objects.filter(id=k.id).update(kmeansharga=kmeanshargasss[i])
        #     i += 1
        kategori = get_object_or_404(Kategori, id=kategori_id)
        produks = produks.filter(kategori=kategori)
        query = request.GET.get("search_produk")
        if query:
            produks = Produk.objects.filter(nama__icontains=query).filter(kategori=kategori_id)  # .order_by('-id')[:9:1]
    return render(request, 'shop/produk/list.html', {'kategori': kategori, 'kategoris': kategoris,
                                                     'produks': produks, 'rekomendasi':rekomendasi})


def produk_detail(request, kategori_id, id):
    produk = get_object_or_404(Produk, kategori_id=kategori_id, id=id, available=True)
    hargaakhir = produk.harga - (produk.harga * produk.diskon / 100)
    ratings = Ratingproduk.objects.all().filter(produk_id=id).aggregate(sum=Sum('ratingproduk'))['sum']
    count = Ratingproduk.objects.all().filter(produk_id=id).count()
    if count == 0:
        rating = 'belum tersedia'
    else:
        rating = ratings / count
    return render(request, 'shop/produk/detail.html',
                  {'produk': produk, 'hargaakhir': hargaakhir, 'rating': rating})


# @login_required(login_url=settings.LOGIN_URL)
def addproduk(request):
    if request.method == 'POST':
        form = CreatePrudukForm(request.POST)
        if form.is_valid():
            current_user = request.user
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
            toko = Toko.objects.get(pelanggan_id=pelanggan.id)

            produk = Produk.objects.create(kategori=form.cleaned_data['kategori'],
                                           nama=form.cleaned_data['nama'],
                                           gambar=form.cleaned_data['gambar'],
                                           deskripsi=form.cleaned_data['deskripsi'],
                                           harga=form.cleaned_data['harga'],
                                           stok=form.cleaned_data['stok'],
                                           available=form.cleaned_data['available'],
                                           diskon=form.cleaned_data['diskon'],
                                           toko_id_id=toko.id)
        return HttpResponseRedirect('/toko-saya/')
    context = {
        'form': CreatePrudukForm,
    }
    return render(request, 'shop/produk/add_produk.html', context)
