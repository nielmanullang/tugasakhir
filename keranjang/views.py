from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Produk
from .keranjang import Keranjang
from .forms import KeranjangTambahProdukForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

@require_POST
@login_required(login_url=settings.LOGIN_URL)
def keranjang_tambah(request, produk_id):
    keranjang = Keranjang(request)
    produk = get_object_or_404(Produk, id=produk_id)
    form = KeranjangTambahProdukForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        keranjang.tambah(produk=produk,
                 jumlah=cd['jumlah'],
                 update_jumlah=cd['update'])
    return redirect('keranjang:keranjang_detail')

def keranjang_hapus(request, produk_id):
    keranjang = Keranjang(request)
    produk = get_object_or_404(Produk, id=produk_id)
    keranjang.hapus(produk)
    return redirect('keranjang:keranjang_detail')

def keranjang_detail(request):
    keranjang = Keranjang(request)
    for item in keranjang:
        item['update_jumlah_form'] = KeranjangTambahProdukForm(initial={'jumlah': item['jumlah'], 'update': True})
    return render(request, 'keranjang/detail.html', {'keranjang': keranjang})

