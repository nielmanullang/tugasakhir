from django.shortcuts import render
from pelanggan.models import Pelanggan

# Create your views here.

def profil(request):
    if request.user.is_authenticated():
        current_user = request.user
        pelanggan = Pelanggan.objects.filter(user_id=current_user.id)
    else:
        return render(request, 'create_pelanggan.html')
    return render(request, 'profil.html', {'pelanggan':pelanggan})