from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^addpelanggan/$', views.create_pelanggan, name='createpelanggan'),
]
