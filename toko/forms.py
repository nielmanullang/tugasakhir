from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class CreateTokoForm(forms.Form):
    nama = forms.CharField(label='Nama', max_length=30)
    slogan = forms.CharField(label='Slogan', max_length=100)
    deskripsi = forms.CharField(label='Deskripsi', max_length=250)