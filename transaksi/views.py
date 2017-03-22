from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
# from .tasks import order_created
from keranjang.keranjang import Keranjang


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
        form = OrderCreateForm()
    return render(request, 'transaksi/order/create.html', {'keranjang': keranjang,
                                                        'form': form})
