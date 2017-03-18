from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from homepage.forms import *
from django.contrib.auth.models import User
from pelanggan.models import Pelanggan, Akun
from django.template import RequestContext
from django.shortcuts import render_to_response


# Create your views here.
def login_view(request):
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                try:
                    akun = Akun.objects.get(akun=user.id)
                    login(request, user)

                    request.session['pelanggan_id'] = akun.pelanggan.id
                    request.session['jenis_akun'] = akun.jenis_akun
                    request.session['username'] = request.POST['username']
                except:
                    messages.add_message(request, messages.INFO,
                                         'Akun ini belum terhubung dengan data pelanggan, silahkan hubungi administrator')
                return redirect('/')
            else:
                messages.add_message(request, messages.INFO, 'User belum terverifikasi')
        else:
            messages.add_message(request, messages.INFO, 'Username atau password Anda salah')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            pelanggan = Pelanggan.objects.create(nama=form.cleaned_data['nama'],
                                                 no_telpon=form.cleaned_data['no_telpon'],
                                                 jenis_kelamin=form.cleaned_data['jenis_kelamin'],
                                                 kabupaten=form.cleaned_data['kabupaten'],
                                                 alamat=form.cleaned_data['alamat'],
                                                 kodepos=form.cleaned_data['kodepos'], )
            akun = Akun.objects.create(akun=form.cleaned_data['akun'], pelanggan=form.cleaned_data['pelanggan'],
                                       jenis_akun=form.cleaned_data['jenis_akun'], )
        return HttpResponseRedirect('/')
    form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)
