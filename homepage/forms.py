from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password (Again)', widget=forms.PasswordInput)
    nama = forms.CharField(label='Nama', max_length=100)
    no_telpon = forms.CharField(label='No Telpon', max_length=30)
    jenis_kelamin = forms.CharField(label='Jenis Kelamin' , max_length=30)
    kabupaten = forms.CharField(label='Kabupaten', max_length=32)
    alamat = forms.CharField(label='Alamat', max_length=100)
    kodepos = forms.CharField(label='Kode Pos', max_length=5)


    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only containalphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')