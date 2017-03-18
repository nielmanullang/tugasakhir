from django.shortcuts import render, get_object_or_404
from .models import Kategori, Produk
from keranjang.forms import KeranjangTambahProdukForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

# @login_required(login_url=settings.LOGIN_URL)
def produk_list(request, kategori_slug=None):
    kategori = None
    kategoris = Kategori.objects.all()
    produks = Produk.objects.filter(available=True)
    if kategori_slug:
        kategori = get_object_or_404(Kategori, slug=kategori_slug)
        produks = produks.filter(kategori=kategori)
    return render(request, 'shop/produk/list.html', {'kategori': kategori, 'kategoris': kategoris, 'produks': produks})

def produk_detail(request, id, slug):
    produk = get_object_or_404(Produk, id=id, slug=slug, available=True)
    keranjang_produk_form = KeranjangTambahProdukForm()
    return render(request, 'shop/produk/detail.html', {'produk': produk, 'keranjang_produk_form': keranjang_produk_form })
