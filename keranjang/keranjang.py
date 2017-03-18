from decimal import Decimal
from django.conf import settings
from shop.models import Produk

class Keranjang(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        keranjang = self.session.get(settings.KERANJANG_SESSION_ID)
        if not keranjang:
            # save an empty cart in the session
            keranjang = self.session[settings.KERANJANG_SESSION_ID] = {}
        self.keranjang = keranjang

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['jumlah'] for item in self.keranjang.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        produk_ids = self.keranjang.keys()
        # get the product objects and add them to the cart
        produks = Produk.objects.filter(id__in=produk_ids)
        for produk in produks:
            self.keranjang[str(produk.id)]['produk'] = produk

        for item in self.keranjang.values():
            item['harga'] = Decimal(item['harga'])
            item['total_harga'] = item['harga'] * item['jumlah']
            yield item

    def tambah(self, produk, jumlah=1, update_jumlah=False):
        """
        Add a product to the cart or update its quantity.
        """
        produk_id = str(produk.id)
        if produk_id not in self.keranjang:
            self.keranjang[produk_id] = {'jumlah': 0,
                                      'harga': str(produk.harga)}
        if update_jumlah:
            self.keranjang[produk_id]['jumlah'] = jumlah
        else:
            self.keranjang[produk_id]['jumlah'] += jumlah
        self.simpan()

    def hapus(self, produk):
        """
        Remove a product from the cart.
        """
        produk_id = str(produk.id)
        if produk_id in self.keranjang:
            del self.keranjang[produk_id]
            self.simpan()

    def simpan(self):
        # update the session cart
        self.session[settings.KERANJANG_SESSION_ID] = self.keranjang
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def kosongkan(self):
        # empty cart
        self.session[settings.KERANJANG_SESSION_ID] = {}
        self.session.modified = True

    def get_total_harga(self):
        return sum(Decimal(item['harga']) * item['jumlah'] for item in self.keranjang.values())
