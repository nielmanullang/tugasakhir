from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.produk_list_toko, name='produk_list_toko'),
    url(r'^(?P<toko_slug>[-\w]+)/$', views.produk_list_toko, name='produk_list_by_toko'),
    url(r'^register_toko/$', views.register_toko, name='register_toko'),
    url(r'^(?P<toko>\d+)/(?P<slug>[-\w]+)/$', views.toko_profil, name='toko_profil'),
]
