from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, CustomZarejestrujForm
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import UserProfile
from django.http import JsonResponse
from django.contrib.auth.models import User

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'exists': User.objects.filter(username=username).exists()
    }
    return JsonResponse(data)

def register(request):
    if request.method == 'POST':
        form = CustomZarejestrujForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            login(request, user)
            return redirect('home')
    else:
        form = CustomZarejestrujForm()
    return render(request, 'account/signup.html', {'form': form})

@login_required
def edytuj_profil(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('konta:profil')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'konta/edycja_profil.html', {'form': form})

@login_required
def usun_konto(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('/')
    return render(request, 'konta/usun_konto.html')

@login_required
def profil(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'konta/profil.html', {'profile': profile})