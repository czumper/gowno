from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profil(request):
    return render(request, 'konta/profil.html', {'user': request.user})
# Create your views here.
