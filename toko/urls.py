from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.produk_list_toko, name='produk_list_toko'),
    url(r'^(?P<toko_id>[-\w]+)/$', views.produk_list_toko, name='produk_list_by_toko'),
    url(r'^register_toko/$', views.register_toko, name='register_toko'),
    # url(r'^toko-saya/(?P<id>\d+)/$', views.toko_profil, name='toko_profil'),
    # url(r'^(?P<toko>\d+)/(?P<id>[-\w]+)/$', views.toko_profil, name='toko_profil'),
    #url(r'^(?P<kategori_id>[-\w]+)/(?P<id>\d+)/$', views.produk_detail, name='produk_detail'),
]
