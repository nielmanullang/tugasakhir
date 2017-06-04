from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.decisiontree, name='decisiontree'),
    url(r'^$', views.pre_handphone, name='pre_handphone'),
    url(r'^$', views.pre_kulkas, name='pre_kulkas'),
    url(r'^$', views.pre_televisi, name='pre_kulkas'),
    url(r'^$', views.variabeltelevisi, name='variabeltelevisi'),
    url(r'^$', views.variabelkulkas, name='variabelkulkas'),
    url(r'^$', views.variabelhandphone, name='variabelhandphone'),
    url(r'^$', views.variabelsemuakategori, name='variabelsemuakategori'),
    url(r'^$', views.prediksi, name='prediksi'),
]
