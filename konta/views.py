from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, CustomZarejestrujForm
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import UserProfile
from django.http import JsonResponse
from django.contrib.auth.models import User
from allauth.account.views import SignupView


class CustomZarejestrujView(SignupView):
    form_class = CustomZarejestrujForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Ten email jest już zajęty.')
            return self.form_invalid(form)
        # Jeśli email jest unikalny, zapisz użytkownika
        self.user = form.save(self.request)
        send_email_confirmation(self.request, self.user, signup=True)
        return redirect(self.get_success_url())
    
def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'exists': User.objects.filter(username=username).exists()
    }
    return JsonResponse(data)


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