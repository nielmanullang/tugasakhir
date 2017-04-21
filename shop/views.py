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
    produks = Produk.objects.filter(available=True)#.order_by('-id')[:9:1]
    query = request.GET.get("search_produk")
    if query:
        produks = Produk.objects.filter(nama__icontains=query)
        #     .count()
        # total = produks / 2
        # if total % 2 == 0:
        #     if (total < total):
        #         kategoriharga = 'murah'
        #     else:
        #         kategoriharga = 'mahal'
        # else:
        #     if (total < total):
        #         kategoriharga = 'murah'
        #     else:
        #         kategoriharga = 'mahal'
    if kategori_id:
        kategori = get_object_or_404(Kategori, id=kategori_id)
        produks = produks.filter(kategori=kategori)
        query = request.GET.get("search_produk")
        if query:
            produks = Produk.objects.filter(nama__icontains=query).filter(kategori=kategori_id)#.order_by('-id')[:9:1]
            # if total % 2 == 0:
            #     if (total < total):
            #         kategoriharga = 'murah'
            #     else:
            #         kategoriharga = 'mahal'
            # else:
            #     if (total < total):
            #         kategoriharga = 'murah'
            #     else:
            #         kategoriharga = 'mahal'
    return render(request, 'shop/produk/list.html', {'kategori': kategori, 'kategoris': kategoris, 'produks': produks})#, 'kategoriharga':kategoriharga})

#@login_required(login_url=settings.LOGIN_URL)
def produk_detail(request, kategori_id, id):
    produk = get_object_or_404(Produk, kategori_id=kategori_id, id=id, available=True)
    hargaakhir = produk.harga - (produk.harga * produk.diskon / 100)
    ratings = Ratingproduk.objects.all().filter(produk_id=id).aggregate(sum=Sum('ratingproduk'))['sum']
    count = Ratingproduk.objects.all().filter(produk_id=id).count()
    if count == 0:
        rating = 'belum tersedia'
    else:
        rating = ratings/count
    return render(request, 'shop/produk/detail.html', {'produk': produk, 'hargaakhir':hargaakhir, 'rating':rating})


#@login_required(login_url=settings.LOGIN_URL)
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
        return HttpResponseRedirect('/toko-saya/')
    context = {
        'form': CreatePrudukForm,
    }
    return render(request, 'shop/produk/add_produk.html', context)
