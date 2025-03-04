from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        return None  # Nie tworzymy User od razu

    def get_signup_redirect_url(self, request):
        return '/accounts/confirm-email/'  # Przekierowanie po rejestracji

    def login(self, request, user):
        # Blokujemy logowanie przed weryfikacją
        return HttpResponseRedirect('/accounts/confirm-email/')