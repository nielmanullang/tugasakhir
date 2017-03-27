from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
# from .tasks import order_created
from keranjang.keranjang import Keranjang
from django.contrib.auth.models import User
from pelanggan.models import Pelanggan
from transaksi.models import Order

def order_create(request):
    keranjang = Keranjang(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in keranjang:
                OrderItem.objects.create(order=order,
                                         produk=item['produk'],
                                         harga=item['harga'],
                                         jumlah=item['jumlah'])
            # clear the cart
            keranjang.kosongkan()
            # launch asynchronous task
            # order_created.delay(order.id)
            return render(request, 'transaksi/order/created.html', {'order': order})
    else:
        current_user = request.user
        user = User.objects.get(id=current_user.id)
        pelanggan = Pelanggan.objects.get(user_id=current_user.id)
        orders = Order.objects.create(nama=pelanggan.nama,
                                   email=user.email,
                                   alamat=pelanggan.alamat,
                                   kabupaten=pelanggan.kabupaten,
                                   kodepos=pelanggan.kodepos)
#        form = OrderCreateForm()
    context = {
        'form': OrderCreateForm,
    }
    return render(request, 'transaksi/order/create.html', context) #'keranjang': keranjang, 'form': form})