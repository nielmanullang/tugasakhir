from .keranjang import Keranjang

def keranjang(request):
    return {'keranjang': Keranjang(request) }
