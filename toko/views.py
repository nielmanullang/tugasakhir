from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pelanggan.models import Pelanggan
from toko.models import Toko
from shop.models import Produk
from django.contrib import messages


def produk_list_toko(request, toko_slug=None):
    toko = None
    tokos = Toko.objects.all()
    produks = Produk.objects.filter(available=True)
    if toko_slug:
        toko = get_object_or_404(Toko, slug=toko_slug)
        produks = produks.filter(toko_id=toko)
    return render(request, 'toko/list.html', {'toko': toko, 'tokos': tokos, 'produks': produks})


def toko_profil(request, toko_slug=None):
    if request.user.is_authenticated():
        toko = Toko.objects.get(id=request.session['pelanggan_id'])
        produks = Produk.objects.filter(toko_id=toko.id)
    else:
        return render(request, 'toko/create_toko.html')
        # return redirect('/toko/')
    return render(request, 'toko/toko_profil.html', {"toko": toko, "produk": produks})
