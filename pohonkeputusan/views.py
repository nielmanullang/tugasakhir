from django.shortcuts import render
from pohonkeputusan.models import Pohonkeputusan
from shop.models import Produk
from pesan.models import Pesan
from pelanggan.models import Pelanggan
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


# Create your views here.
def decisiontree(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    # userlogin untuk mencari data yang login
    userlogin = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id)
    count = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id).count()

    if count > 0:
        df = read_frame(userlogin,
                        fieldnames=['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko', 'label'])
        X = df.iloc[:, [0, 1, 2, 3, 4]].values
        Y = df.iloc[:, [5]].values
        X_count = userlogin.count()

        produk = Produk.objects.all().filter(kategori_id=3).order_by('id')
        df_xtrain = read_frame(produk,
                               fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon',
                                           'kategoriratingproduk',
                                           'kategoriratingtoko'])
        X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values

        # Fitting Decision Tree Classification to the Training set
        classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
        clf = classifier.fit(X, Y)

        # Predicting the Test set results
        y_pred = classifier.predict(X_xtrain)

        dot_data = tree.export_graphviz(clf, out_file=None)
        graph = pydotplus.graph_from_dot_data(dot_data)
        graph.write_png(current_user.username + '.PNG')
    else:
        return render(request, 'pohonkeputusan/belumadatree.html', {'pelanggan': pelanggan})

    return render(request, 'pohonkeputusan/decisiontree.html',
                  {'X': X, 'Y': Y, 'clf': clf, 'pelanggan': pelanggan, 'userlogin': userlogin,
                   'X_count': X_count, 'X_xtrain': X_xtrain, 'y_pred': y_pred, 'produk': produk})


def pre_handphone(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    # userlogin untuk mencari data yang login
    userlogin = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id)

    df = read_frame(userlogin,
                    fieldnames=['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko', 'label'])
    X = df.iloc[:, [0, 1, 2, 3, 4]].values
    Y = df.iloc[:, [5]].values
    X_count = userlogin.count()

    # Fitting Decision Tree Classification to the Training set
    classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
    classifier.fit(X, Y)

    produk = Produk.objects.all().filter(kategori_id=3).order_by('id')
    df_xtrain = read_frame(produk,
                           fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon', 'kategoriratingproduk',
                                       'kategoriratingtoko'])
    X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values

    # Predicting the Test set results
    y_pred = classifier.predict(X_xtrain)

    return render(request, 'pohonkeputusan/prediksihandphone.html',
                  {'X': X, 'Y': Y, 'pelanggan': pelanggan, 'userlogin': userlogin,
                   'X_count': X_count, 'X_xtrain': X_xtrain, 'y_pred': y_pred, 'produk': produk})


@login_required(login_url=settings.LOGIN_URL)
def prediksi(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    countdata = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id).count()
    if countdata > 0:
        userlogin = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id)
        df = read_frame(userlogin,
                        fieldnames=['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko', 'label'])
        X = df.iloc[:, [0, 1, 2, 3, 4]].values
        Y = df.iloc[:, [5]].values
        X_count = userlogin.count()

        # Fitting Decision Tree Classification to the Training set
        classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
        classifier.fit(X, Y)

        produk = Produk.objects.all().order_by('id')
        df_xtrain = read_frame(produk,
                               fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon',
                                           'kategoriratingproduk',
                                           'kategoriratingtoko'])
        X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values
        y_pred = classifier.predict(X_xtrain)
    else:
        sedaerah = Pohonkeputusan.objects.all().filter(perdaerah=pelanggan.kabupaten).count()
        if sedaerah > 0:
            userlogin = Pohonkeputusan.objects.all().filter(perdaerah=pelanggan.kabupaten)
            df = read_frame(userlogin,
                            fieldnames=['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko',
                                        'label'])
            X = df.iloc[:, [0, 1, 2, 3, 4]].values
            Y = df.iloc[:, [5]].values
            X_count = userlogin.count()

            # Fitting Decision Tree Classification to the Training set
            classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
            classifier.fit(X, Y)

            produk = Produk.objects.all().order_by('id')
            df_xtrain = read_frame(produk,
                                   fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon',
                                               'kategoriratingproduk',
                                               'kategoriratingtoko'])
            X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values
            y_pred = classifier.predict(X_xtrain)
        else:
            return render(request, 'pohonkeputusan/tidakadarekomendasi.html',{'pelanggan':pelanggan})
    return render(request, 'pohonkeputusan/adarekomendasi.html',
                  {'X': X, 'Y': Y, 'pelanggan': pelanggan, 'userlogin': userlogin,
                   'X_count': X_count, 'X_xtrain': X_xtrain, 'y_pred': y_pred, 'produk': produk})


def pre_televisi(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    # userlogin untuk mencari data yang login
    userlogin = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id)

    df = read_frame(userlogin,
                    fieldnames=['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko', 'label'])
    X = df.iloc[:, [0, 1, 2, 3, 4]].values
    Y = df.iloc[:, [5]].values
    X_count = userlogin.count()

    produk = Produk.objects.all().filter(kategori_id=4).order_by('id')
    df_xtrain = read_frame(produk,
                           fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon', 'kategoriratingproduk',
                                       'kategoriratingtoko'])
    X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values

    # Fitting Decision Tree Classification to the Training set
    classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
    clf = classifier.fit(X, Y)

    # Predicting the Test set results
    y_pred = classifier.predict(X_xtrain)

    return render(request, 'pohonkeputusan/prediksitelevisi.html',
                  {'X': X, 'Y': Y, 'clf': clf, 'pelanggan': pelanggan, 'userlogin': userlogin,
                   'X_count': X_count, 'X_xtrain': X_xtrain, 'y_pred': y_pred, 'produk': produk})


def pre_kulkas(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    # userlogin untuk mencari data yang login
    userlogin = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id)

    df = read_frame(userlogin,
                    fieldnames=['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko', 'label'])
    X = df.iloc[:, [0, 1, 2, 3, 4]].values
    Y = df.iloc[:, [5]].values
    X_count = userlogin.count()

    produk = Produk.objects.all().filter(kategori_id=5).order_by('id')
    df_xtrain = read_frame(produk,
                           fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon', 'kategoriratingproduk',
                                       'kategoriratingtoko'])
    X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values

    # Fitting Decision Tree Classification to the Training set
    classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
    clf = classifier.fit(X, Y)

    # Predicting the Test set results
    y_pred = classifier.predict(X_xtrain)

    return render(request, 'pohonkeputusan/prediksikulkas.html',
                  {'X': X, 'Y': Y, 'clf': clf, 'pelanggan': pelanggan, 'userlogin': userlogin,
                   'X_count': X_count, 'X_xtrain': X_xtrain, 'y_pred': y_pred, 'produk': produk})


def variabeltelevisi(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    produk = Produk.objects.all().filter(kategori_id=4).order_by('id')
    df_xtrain = read_frame(produk,
                           fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon', 'kategoriratingproduk',
                                       'kategoriratingtoko'])
    X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values

    return render(request, 'pohonkeputusan/variabeltelevisi.html',
                  {'pelanggan': pelanggan, 'X_xtrain': X_xtrain, 'produk': produk})


def variabelkulkas(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    produk = Produk.objects.all().filter(kategori_id=5).order_by('id')
    df_xtrain = read_frame(produk,
                           fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon', 'kategoriratingproduk',
                                       'kategoriratingtoko'])
    X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values

    return render(request, 'pohonkeputusan/variabelkulkas.html',
                  {'pelanggan': pelanggan, 'X_xtrain': X_xtrain, 'produk': produk})


def variabelhandphone(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    produk = Produk.objects.all().filter(kategori_id=3).order_by('id')
    df_xtrain = read_frame(produk,
                           fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon', 'kategoriratingproduk',
                                       'kategoriratingtoko'])
    X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values

    return render(request, 'pohonkeputusan/variabelhandphone.html',
                  {'pelanggan': pelanggan, 'X_xtrain': X_xtrain, 'produk': produk})


def variabelsemuakategori(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    produk = Produk.objects.all().order_by('id')
    df_xtrain = read_frame(produk,
                           fieldnames=['kmeansharga', 'kategoriongkoskirim', 'kategoridiskon', 'kategoriratingproduk',
                                       'kategoriratingtoko'])
    X_xtrain = df_xtrain.iloc[:, [0, 1, 2, 3, 4]].values

    return render(request, 'pohonkeputusan/variabelsemuakategori.html',
                  {'pelanggan': pelanggan, 'X_xtrain': X_xtrain, 'produk': produk})
