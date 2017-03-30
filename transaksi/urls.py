from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    # url(r'^create/(?P<produk_id>[-\w]+)$', views.beli_create, name='beli_create'),
    url(r'^beli/(?P<produk_id>[0-9a-z-]+)/(?P<pelanggan_id>[0-9a-z-]+)$',views.beli,name='beli')
]
