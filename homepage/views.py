from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from homepage.forms import *
from django.contrib.auth.models import User
from pelanggan.models import Pelanggan
from django.template import RequestContext
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
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Count

# Create your views here.
def login_view(request):
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                try:
                    akun = User.objects.get(id=user.id)
                    login(request, user)

                    # request.session['user_id'] = akun.pelanggan.id
                    # request.session['username'] = request.POST['username']

                    # rekomendasi insert to table
                    produks = Produk.objects.filter(available=True)  # .order_by('-id')[:9:1]
                    current_user = request.user
                    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
                    countdata = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id).count()
                    if countdata > 0:
                        userlogin = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id)
                        df = read_frame(userlogin,
                                        fieldnames=['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk',
                                                    'ratingtoko', 'label'])
                        X = df.iloc[:, [0, 1, 2, 3, 4]].values
                        Y = df.iloc[:, [5]].values

                        # Fitting Decision Tree Classification to the Training set
                        classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
                        classifier.fit(X, Y)

                        produks = Produk.objects.all().order_by('id')
                        df_xtrain = read_frame(produks,
                                               fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon',
                                                           'kategoriratingproduk',
                                                           'kategoriratingtoko'])
                        X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values
                        y_pred = classifier.predict(X_xtrain)
                        i = 0
                        for produk in produks:
                            rekomendasi = Rekomendasi.objects.create(produk_id=produk.id,
                                                                     produk_kategori=produk.kategori_id,
                                                                     produk_nama=produk.nama,
                                                                     produk_gambar=produk.gambar,
                                                                     produk_harga=produk.harga,
                                                                     produk_diskon=produk.diskon,
                                                                     n_harga=X_xtrain[i][0],
                                                                     n_ongkir=X_xtrain[i][1],
                                                                     n_diskon=X_xtrain[i][2],
                                                                     n_ratingproduk=X_xtrain[i][3],
                                                                     n_ratingtoko=X_xtrain[i][4],
                                                                     prediksi=y_pred[i],
                                                                     pelanggan=pelanggan.id)
                            i=i+1
                    else:
                        current_user = request.user
                        pelanggan = Pelanggan.objects.get(user_id=current_user.id)
                        sedaerah = Pohonkeputusan.objects.all().filter(perdaerah=pelanggan.kabupaten).count()
                        if sedaerah > 0:
                            userlogin = Pohonkeputusan.objects.all().filter(perdaerah=pelanggan.kabupaten).order_by(
                                '-label').values_list('kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk',
                                                      'ratingtoko').distinct()
                            df = read_frame(userlogin,
                                            fieldnames=['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk',
                                                        'ratingtoko',
                                                        'label'])
                            X = df.iloc[:, [0, 1, 2, 3, 4]].values
                            Y = df.iloc[:, [5]].values

                            # Fitting Decision Tree Classification to the Training set
                            classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
                            classifier.fit(X, Y)

                            produks = Produk.objects.all().order_by('id')
                            df_xtrain = read_frame(produks,
                                                   fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon',
                                                               'kategoriratingproduk',
                                                               'kategoriratingtoko'])
                            X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values
                            y_pred = classifier.predict(X_xtrain)

                            i = 0
                            for produk in produks:
                                rekomendasi = Rekomendasi.objects.create(produk_id=produk.id,
                                                                         produk_kategori=produk.kategori_id,
                                                                         produk_nama=produk.nama,
                                                                         produk_gambar=produk.gambar,
                                                                         produk_harga=produk.harga,
                                                                         produk_diskon=produk.diskon,
                                                                         n_harga=X_xtrain[i][0],
                                                                         n_ongkir=X_xtrain[i][1],
                                                                         n_diskon=X_xtrain[i][2],
                                                                         n_ratingproduk=X_xtrain[i][3],
                                                                         n_ratingtoko=X_xtrain[i][4],
                                                                         prediksi=y_pred[i],
                                                                         pelanggan=pelanggan.id)
                                i=i+1
                    #end rekomendasi insert to table
                except:
                    messages.add_message(request, messages.INFO,
                                         'Akun ini belum terhubung dengan data pelanggan, silahkan hubungi administrator')
                return redirect('/')
            else:
                messages.add_message(request, messages.INFO, 'User belum terverifikasi')
        else:
            messages.add_message(request, messages.INFO, 'Username atau password Anda salah')
    return render(request, 'login.html')


def logout_view(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    Rekomendasi.objects.filter(pelanggan=pelanggan.id).delete()
    logout(request)
    return redirect('/login/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data['username'],
                                       email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password1'], )
            user.save()
            # pelanggan = Pelanggan.objects.create(nama=form.cleaned_data['nama'],
            #                                      no_telepon=form.cleaned_data['no_telpon'],
            #                                      jenis_kelamin=form.cleaned_data['jenis_kelamin'],
            #                                      kabupaten=form.cleaned_data['kabupaten'],
            #                                      alamat=form.cleaned_data['alamat'],
            #                                      kodepos=form.cleaned_data['kodepos'],
            #                                      user_id_id=user.id)
        return HttpResponseRedirect('/')
    form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)
