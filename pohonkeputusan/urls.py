from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.decisiontree, name='decisiontree'),
    url(r'^$', views.pre_handphone, name='pre_handphone'),
    url(r'^$', views.pre_kulkas, name='pre_kulkas'),
    url(r'^$', views.pre_televisi, name='pre_kulkas'),
    url(r'^$', views.prediksi, name='prediksi'),
]
