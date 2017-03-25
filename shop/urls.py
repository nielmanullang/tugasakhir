from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.produk_list, name='produk_list'),
    url(r'^(?P<kategori_id>[-\w]+)/$', views.produk_list, name='produk_list_by_kategori'),
    url(r'^(?P<id>\d+)/(?P<kategori_id>[-\w]+)/$', views.produk_detail, name='produk_detail'),
    url(r'^addproduk/$', views.addproduk, name='addproduk'),
]
