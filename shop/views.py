from django.shortcuts import render, get_object_or_404
from .models import Kategori, Produk
from keranjang.forms import KeranjangTambahProdukForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import CreatePrudukForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from pelanggan.models import Pelanggan
from toko.models import Toko


#@login_required(login_url=settings.LOGIN_URL)
def produk_list(request, kategori_id=None):
    kategori = None
    kategoris = Kategori.objects.all()
    produks = Produk.objects.filter(available=True)
    if kategori_id:
        kategori = get_object_or_404(Kategori, id=kategori_id)
        produks = produks.filter(kategori=kategori)
    return render(request, 'shop/produk/list.html', {'kategori': kategori, 'kategoris': kategoris, 'produks': produks})

#@login_required(login_url=settings.LOGIN_URL)
def produk_detail(request, id, kategori_id):
    produk = get_object_or_404(Produk, id=id, kategori_id=kategori_id, available=True)
    keranjang_produk_form = KeranjangTambahProdukForm()
    return render(request, 'shop/produk/detail.html', {'produk': produk, 'keranjang_produk_form': keranjang_produk_form })

def addproduk(request):
    if request.method == 'POST':
        form = CreatePrudukForm(request.POST)
        if form.is_valid():
            current_user = request.user
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
            toko = Toko.objects.get(pelanggan_id=pelanggan.id)

            produk = Produk.objects.create(kategori=form.cleaned_data['kategori'],
                                           nama=form.cleaned_data['nama'],
                                           gambar=form.cleaned_data['gambar'],
                                           deskripsi=form.cleaned_data['deskripsi'],
                                           harga=form.cleaned_data['harga'],
                                           stok=form.cleaned_data['stok'],
                                           available=form.cleaned_data['available'],
                                           diskon=form.cleaned_data['diskon'],
                                           toko_id_id=toko.id)
        return HttpResponseRedirect('/')
    context = {
        'form': CreatePrudukForm,
    }

    return render(request, 'shop/produk/add_produk.html', context)
