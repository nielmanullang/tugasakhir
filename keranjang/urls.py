from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.keranjang_detail, name='keranjang_detail'),
    url(r'^tambah/(?P<produk_id>\d+)/$', views.keranjang_tambah, name='keranjang_tambah'),
    url(r'^hapus/(?P<produk_id>\d+)/$', views.keranjang_hapus, name='keranjang_hapus'),
]
