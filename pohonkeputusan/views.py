from django.shortcuts import render
from pohonkeputusan.models import Pohonkeputusan
from shop.models import Produk
from pesanan.models import Pesanan
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
import csv
from django.http import HttpResponse

# Create your views here.
def decisiontree(request):
    current_user = request.user
    pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    #pesanan = Pesanan.objects.filter(pelanggan_id=pelanggan.id).order_by('-id')[0]
    # qs untuk mencari data yang login dan pelanggan ber id 0
    qa = Pohonkeputusan.objects.all().filter(pelanggan=0)
    qb = Pohonkeputusan.objects.all().filter(pelanggan=pelanggan.id)
    qs = qa | qb

    # # kmeans
    # # Importing the dataset untuk harga
    # dff = read_frame(kategori, fieldnames=['nama', 'gambar', 'deskripsi', 'harga', 'diskon', 'stok', 'available'])
    # Z = dff.iloc[:, [4]].values
    # # Fitting K-Means to the dataset
    # kmeans = KMeans(n_clusters=2, init='k-means++', random_state=42)
    # y_kmeans = kmeans.fit_predict(Z)
    df = read_frame(qs, fieldnames=['kategoriharga', 'ongkoskirim', 'diskon', 'ratingproduk', 'ratingtoko', 'label'])
    X = df.iloc[:, [0, 1, 2, 3, 4]].values
    Y = df.iloc[:, [5]].values
    X_count = qs.count()

    #gakpenting
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=0)
    X_train_count = X_train.shape
    Y_train_count2 = Y_train.shape

    # Fitting Decision Tree Classification to the Training set
    classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
    clf = classifier.fit(X, Y)

    # Predicting the Test set results / gakpenting
    y_pred = classifier.predict(X_test)

    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_png(current_user.username + '.PNG')

    return render(request, 'pohonkeputusan/decisiontree.html',
                  {'X': X, 'Y': Y, 'X_train': X_train, 'Y_train': Y_train, 'X_train_count': X_train_count,
                   'Y_train_count2': Y_train_count2, 'clf': clf, 'y_pred': y_pred, 'pelanggan': pelanggan, 'qs': qs,
                   'X_count': X_count})


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response