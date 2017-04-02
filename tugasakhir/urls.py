"""tugasakhir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from homepage import views as homepage_views
from pelanggan import views as pelanggan_views
from toko import views as toko_views
from shop import views as shop_views
from transaksi import views as transaksi_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^pelanggan/', pelanggan_views.profil),
    url(r'^pembelian/', transaksi_views.pembelian),
    url(r'^penjualan/', transaksi_views.penjualan),
    url(r'^toko-saya/', toko_views.toko_profil),
    url(r'^addproduk/', shop_views.addproduk),
    url(r'^register_toko/', toko_views.register_toko),
    url(r'^pelanggan-create/', pelanggan_views.create_pelanggan),
    url(r'^toko/', include ('toko.urls', namespace='toko')),
    url(r'^transaksi/', include('transaksi.urls', namespace='transaksi')),
    url(r'^login/', homepage_views.login_view),
    url(r'^register/', homepage_views.register_page),
    url(r'^logout/', homepage_views.logout_view),
    url(r'^', include('shop.urls', namespace='shop')),
    url(r'^beli/',transaksi_views.beli),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
