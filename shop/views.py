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
from django.shortcuts import render_to_response
from pohonkeputusan.models import Pohonkeputusan
from shop.models import Produk, Rekomendasi
from pesan.models import Pesan
import psycopg2 as pg
import pandas.io.sql as psql
from django_pandas.io import read_frame
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import pydotplus
from sklearn.cluster import KMeans
from django_pandas.io import read_frame
import numpy as np
from django.http import HttpResponse
from django.db.models import Count

# @login_required(login_url=settings.LOGIN_URL)
def produk_list(request, kategori_id=None):
    kategori = None
    kategoris = Kategori.objects.all()
    produks = Produk.objects.filter(available=True)  # .order_by('-id')[:9:1]
    # untuk mengupdate kategori ongkos kirim berdasarkan yang login
    current_user = request.user
    if (current_user is not None):
        try:
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        except Pelanggan.DoesNotExist:
            pelanggan = None
        if (pelanggan is not None):
            rekomendasi = Rekomendasi.objects.filter(prediksi=1, pelanggan=pelanggan.id)
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
            #loop produk untuk update rating
            orderproduks = Produk.objects.all().order_by('id')
            for produk in orderproduks:
                ratingproduks = Ratingproduk.objects.all().filter(produk_id_id=produk.id).aggregate(sum=Sum('ratingproduk'))['sum']
                count = Ratingproduk.objects.all().filter(produk_id_id=produk.id).count()
                if count == 0:
                    ratingproduk = 0
                else:
                    ratingproduk = ratingproduks / count
                ratingtokos = Ratingtoko.objects.all().filter(toko_id_id=produk.toko_id_id).aggregate(sum=Sum('ratingtoko'))['sum']
                counts = Ratingtoko.objects.all().filter(toko_id_id=produk.toko_id_id).count()
                if counts == 0:
                    ratingtoko = 0
                else:
                    ratingtoko = ratingtokos / counts
                produkupdate = Produk.objects.filter(id=produk.id).update(kategoriratingproduk=ratingproduk, kategoriratingtoko=ratingtoko)
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
                kategori = get_object_or_404(Kategori, id=kategori_id)
                produks = produks.filter(kategori=kategori)
                query = request.GET.get("search_produk")
                if query:
                    produks = Produk.objects.filter(nama__icontains=query).filter(kategori=kategori_id)  # .order_by('-id')[:9:1]
            return render(request, 'shop/produk/list.html', {'kategori': kategori, 'kategoris': kategoris, 'pelanggan' : pelanggan,
                                                                 'produks': produks, 'rekomendasi':rekomendasi})
        else:
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

                #loop produk untuk update rating
            orderproduks = Produk.objects.all().order_by('id')
            for produk in orderproduks:
                ratingproduks = Ratingproduk.objects.all().filter(produk_id_id=produk.id).aggregate(sum=Sum('ratingproduk'))['sum']
                count = Ratingproduk.objects.all().filter(produk_id_id=produk.id).count()
                if count == 0:
                    ratingproduk = 0
                else:
                    ratingproduk = ratingproduks / count
                ratingtokos = Ratingtoko.objects.all().filter(toko_id_id=produk.toko_id_id).aggregate(sum=Sum('ratingtoko'))['sum']
                counts = Ratingtoko.objects.all().filter(toko_id_id=produk.toko_id_id).count()
                if counts == 0:
                    ratingtoko = 0
                else:
                    ratingtoko = ratingtokos / counts
                produkupdate = Produk.objects.filter(id=produk.id).update(kategoriratingproduk=ratingproduk, kategoriratingtoko=ratingtoko)
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
                kategori = get_object_or_404(Kategori, id=kategori_id)
                produks = produks.filter(kategori=kategori)
                query = request.GET.get("search_produk")
                if query:
                    produks = Produk.objects.filter(nama__icontains=query).filter(kategori=kategori_id)  # .order_by('-id')[:9:1]
        return render(request, 'shop/produk/list.html', {'kategori': kategori, 'kategoris': kategoris,'produks': produks})


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
