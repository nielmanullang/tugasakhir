from django.shortcuts import render
from pelanggan.models import Pelanggan
from .forms import CreatePelangganForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.
def profil(request):
    if request.user.is_authenticated():
        current_user = request.user
        pelanggan = Pelanggan.objects.filter(user_id=current_user.id)
        return render(request, 'pelanggan/profil.html', {'pelanggan': pelanggan})
    else:
        return render(request, 'pelanggan/create_pelanggan.html')

# @login_required(login_url=settings.LOGIN_URL)
def create_pelanggan(request):
    if request.method == 'POST':
        form = CreatePelangganForm(request.POST)
        if form.is_valid():
            current_user = request.user
            user = User.objects.get(id=current_user.id)
            pelanggan = Pelanggan.objects.create(nama=form.cleaned_data.get('nama'),
                                                 no_telepon=form.cleaned_data.get('no_telepon'),
                                                 jenis_kelamin=form.cleaned_data.get('jenis_kelamin'),
                                                 kabupaten=form.cleaned_data.get('kabupaten'),
                                                 alamat=form.cleaned_data.get('alamat'),
                                                 kodepos=form.cleaned_data.get('kodepos'),
                                                 user_id_id=user.id)
        return HttpResponseRedirect('/')
    context = {
        'form': CreatePelangganForm,
    }
    return render(request, 'pelanggan/create.html', context)
