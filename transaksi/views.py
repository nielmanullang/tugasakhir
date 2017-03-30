from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from .forms import OrderTransaksiForm
from keranjang.keranjang import Keranjang
from django.contrib.auth.models import User
from pelanggan.models import Pelanggan
from transaksi.models import Order
from transaksi.models import Transaksi
from shop.models import Produk


def order_create(request):
    keranjang = Keranjang(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in keranjang:
                orderes = OrderItem.objects.create(order=order,
                                                   produk=item['produk'],
                                                   harga=item['harga'],
                                                   jumlah=item['jumlah'])
                orderes.save()
            # clear the cart
            keranjang.kosongkan()
            # launch asynchronous task
            # order_created.delay(order.id)
            return render(request, 'transaksi/order/created.html', {'orderes': orderes})
    else:
        current_user = request.user
        user = User.objects.get(id=current_user.id)
        pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        orders = Order.objects.create(nama=pelanggan.nama,
                                      email=user.email,
                                      alamat=pelanggan.alamat,
                                      kabupaten=pelanggan.kabupaten,
                                      kodepos=pelanggan.kodepos)
        form = OrderCreateForm()
    return render(request, 'transaksi/order/create.html', {'keranjang': keranjang,
                                                           'form': form})
    # else:
    #     current_user = request.user
    #     user = User.objects.get(id=current_user.id)
    #     pelanggan = Pelanggan.objects.get(user_id=current_user.id)
    #     orders = Order.objects.create(nama=pelanggan.nama,
    #                                   email=user.email,
    #                                   alamat=pelanggan.alamat,
    #                                   kabupaten=pelanggan.kabupaten,
    #                                   kodepos=pelanggan.kodepos)
    # #        form = OrderCreateForm()
    # context = {
    #     'form': OrderCreateForm,
    # }
    # return render(request, 'transaksi/order/created.html', context)  # 'keranjang': keranjang, 'form': form})


def beli_create(request, produk_id):
    keranjang = Keranjang(request)
    if request.method == 'POST':
        form = OrderTransaksiForm(request.POST)
        if form.is_valid():
            current_user = request.user
            #       user = User.objects.get(id=current_user.id)
            pelanggan = Pelanggan.objects.get(user_id=current_user.id)
            produk = get_object_or_404(Produk, id=produk_id)
            orders = Transaksi.objects.create(produk=produk,
                                              biaya_pengiriman=produk.harga,
                                              pelanggan=pelanggan.id,
                                              toko=produk.toko_id)
            orders.save()
        q = Order.objects.filter(id=produk_id).values()
        # return HttpResponseRedirect('')
        return render(request, 'transaksi/order/created.html', {'q': q})
    context = {
        'form': OrderTransaksiForm,
    }
    return render(request, 'transaksi/order/created.html', context)  # 'keranjang': keranjang, 'form': form})

def beli(request, produk_id, pelanggan_id):
    if request.method == 'POST':
        pelanggans = Pelanggan.objects.get(user_id=pelanggan_id)
        produks = Produk.objects.get(id=produk_id)

        transaksi=Transaksi.objects.create(
                                        produk_id=produks.id,
                                        biaya_pengiriman=20,
                                        pelanggan_id=pelanggans.id,
                                        toko=produks.toko_id
        )
    return render(request,'transaksi/order/created.html')