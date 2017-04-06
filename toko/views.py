from toko.models import Toko, Ratingtoko
from shop.models import Produk
from django.http import HttpResponseRedirect
from pelanggan.models import Pelanggan
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import CreateTokoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


def produk_list_toko(request, toko_id=None):
    toko = None
    tokos = Toko.objects.all()
    produks = Produk.objects.filter(available=True)
    ratings = Ratingtoko.objects.all().filter(toko_id=toko_id).aggregate(sum=Sum('ratingtoko'))['sum']
    count = Ratingtoko.objects.all().filter(toko_id=toko_id).count()
    if count == 0:
        rating = ratings
    else:
        rating = ratings / count
    if toko_id:
        toko = get_object_or_404(Toko, id=toko_id)
        produks = produks.filter(toko_id=toko)
    return render(request, 'toko/list.html', {'toko': toko, 'tokos': tokos, 'produks': produks, 'rating':rating, 'count':count})


# @require_POST
@login_required(login_url=settings.LOGIN_URL)
def toko_profil(request):
    current_user = request.user
    if (current_user is not None):
        try:
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        except Pelanggan.DoesNotExist:
            pelanggan = None
        if (pelanggan is not None):
            try:
                toko = Toko.objects.get(pelanggan_id=pelanggan.id)
            except Toko.DoesNotExist:
                toko = None
            if (toko is not None):
                produks = Produk.objects.filter(toko_id=toko.id)
            else:
                return render(request, 'toko/views.html')
        else:
            return render(request, 'toko/toko_null.html')
    else:
        return render(request, 'toko/toko_null.html')
    tokos = Toko.objects.get(pelanggan_id=pelanggan.id)
    ratings = Ratingtoko.objects.all().filter(toko_id=tokos).aggregate(sum=Sum('ratingtoko'))['sum']
    count = Ratingtoko.objects.all().filter(toko_id=tokos).count()
    if count == 0:
        rating = ratings
    else:
        rating = ratings / count
    return render(request, 'toko/toko_profil.html', {'toko': toko, 'produks': produks, 'rating':rating})


@login_required(login_url=settings.LOGIN_URL)
def register_toko(request):
    if request.method == 'POST':
        form = CreateTokoForm(request.POST)
        if form.is_valid():
            current_user = request.user
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
            toko = Toko.objects.create(nama=form.cleaned_data['nama'],
                                       slogan=form.cleaned_data['slogan'],
                                       deskripsi=form.cleaned_data['deskripsi'],
                                       alamat=pelanggan.kabupaten,
                                       pelanggan_id_id=pelanggan.id)
        return HttpResponseRedirect('/')
    context = {
        'form': CreateTokoForm,
    }

    return render(request, 'toko/create.html', context)
