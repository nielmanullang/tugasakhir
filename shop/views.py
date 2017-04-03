from django.shortcuts import render, get_object_or_404
from .models import Kategori, Produk, Ratingproduk
from .forms import CreatePrudukForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from pelanggan.models import Pelanggan
from toko.models import Toko
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Sum

# @login_required(login_url=settings.LOGIN_URL)
def produk_list(request, kategori_id=None):
    kategori = None
    kategoris = Kategori.objects.all()
    produks = Produk.objects.filter(available=True)
    if kategori_id:
        kategori = get_object_or_404(Kategori, id=kategori_id)
        produks = produks.filter(kategori=kategori)
    return render(request, 'shop/produk/list.html', {'kategori': kategori, 'kategoris': kategoris, 'produks': produks})


#@login_required(login_url=settings.LOGIN_URL)
def produk_detail(request, kategori_id, id):
    produk = get_object_or_404(Produk, kategori_id=kategori_id, id=id, available=True)
    hargaakhir = produk.harga - (produk.harga * produk.diskon / 100)
    ratings = Ratingproduk.objects.all().filter(produk_id=id).aggregate(sum=Sum('ratingproduk'))['sum']
    count = Ratingproduk.objects.all().filter(produk_id=id).count()
    if count == 0:
        rating = ratings
    else:
        rating = ratings/count
    return render(request, 'shop/produk/detail.html', {'produk': produk, 'hargaakhir':hargaakhir, 'rating':rating})


@login_required(login_url=settings.LOGIN_URL)
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
                                           diskon=form.cleaned_data['diskon'],
                                           stok=form.cleaned_data['stok'],
                                           available=form.cleaned_data['available'],
                                           toko_id_id=toko.id)
        return HttpResponseRedirect('/')
    context = {
        'form': CreatePrudukForm,
    }
    return render(request, 'shop/produk/add_produk.html', context)
