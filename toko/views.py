from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from pelanggan.models import Pelanggan
from toko.models import Toko
from shop.models import Produk

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
        current_user = request.user
        pelanggan = Pelanggan.objects.filter(user_id=current_user.id)
        toko = Toko.objects.get(pelanggan_id='1')
        # produks = Produk.objects.get(toko_id='1')
    else:
        return render(request, 'toko/create_toko.html')
    return render(request, 'toko/toko_profil.html', {'toko': toko})
