from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^beli/(?P<produk_id>[0-9a-z-]+)/(?P<pelanggan_id>[0-9a-z-]+)$',views.beli,name='beli')
]
