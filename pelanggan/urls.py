from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^pelanggan-create/$', views.create_pelanggan, name='createpelanggan'),
]
