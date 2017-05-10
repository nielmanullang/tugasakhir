from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.decisiontree, name='decisiontree'),
    url(r'^$', views.some_view, name='some_view'),
]
