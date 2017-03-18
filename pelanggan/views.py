from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from pelanggan.models import Pelanggan

# Create your views here.

# @login_required(login_url=settings.LOGIN_URL)
def profil(request):
    pelanggan = Pelanggan.objects.get(id=request.session['pelanggan_id'])
    return render(request, 'profil.html', {"pelanggan":pelanggan})