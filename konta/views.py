from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, CustomSignupForm
from django.contrib.auth import login
from django.contrib.auth import logout, get_user_model
from .models import UserProfile, TempUser
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
"""
from allauth.account.utils import send_email_confirmation
from allauth.account.views import SignupView
from django.http import JsonResponse
from django.core.mail import send_mail
import uuid
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.utils import perform_login
from django.urls import reverse
import logging
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
"""
""""
logger = logging.getLogger(__name__)

class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def form_valid(self, form):
        logger.info("CustomSignupView.form_valid called")
        email = form.cleaned_data.get('email')
        logger.info(f"Email from form: {email}")
        if User.objects.filter(email=email).exists():
            logger.info(f"Email {email} already exists")
            form.add_error('email', 'Ten email jest już zajęty.')
            return self.form_invalid(form)

        logger.info("Saving user")
        self.user = form.save(self.request)

        logger.info("Checking/Updating EmailAddress")
        email_address, created = EmailAddress.objects.get_or_create(
            user=self.user,
            email=email,
            defaults={'primary': True, 'verified': False}
        )
        if not created:
            logger.info(f"EmailAddress for {email} already exists, updating")
            email_address.primary = True
            email_address.verified = False
            email_address.save()

        # Generuj EmailConfirmation
        logger.info("Generating confirmation")
        confirmation = EmailConfirmation.objects.create(
            email_address=email_address,
            sent=datetime.now(),
            created=datetime.now()
        )
        key = confirmation.key
        logger.info(f"Confirmation key: {key}")

        verification_url = self.request.build_absolute_uri(
            reverse('account_confirm_email', args=[key])
        )
        logger.info(f"Verification URL: {verification_url}")

        # Wyślij mail weryfikacyjny z szablonu
        logger.info("Sending verification email")
        email_content = render_to_string(
            'account/email/email_confirmation_message.txt',
            {
                'user': self.user,
                'email': email,
                'activate_url': verification_url,
            }
        )
        email_msg = EmailMessage(
            subject='[pitcernia.ninja] Potwierdź swoje konto',
            body=email_content,
            from_email='webmaster@localhost',
            to=[email],
        )
        email_msg.send(fail_silently=False)

        logger.info("Blocking allauth default email")
        self.request.session['account_email_verification_sent'] = True
        return redirect(self.get_success_url())

    def get_success_url(self):
        return '/accounts/confirm-email/'
"""

User = get_user_model()


@login_required
def profil(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'konta/profil.html', {'profile': profile})
@login_required
def profil(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'konta/profil.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('konta:profil')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'konta/edit_profile.html', {'form': form})
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

def verify_email(request, key):
    try:
        temp_user = TempUser.objects.get(confirmation_key=key)
        # Przenieś do auth_user
        user = User.objects.create_user(
            username=temp_user.username,
            email=temp_user.email,
            password=None  # Hasło jest już zahashowane
        )
        user.password = temp_user.password  # Ustaw zahashowane hasło
        user.save()
        # Zapisz profil
        UserProfile.objects.create(
            user=user,
            ulica=temp_user.ulica,
            numer_domu=temp_user.numer_domu,
            numer_mieszkania=temp_user.numer_mieszkania,
            kod_pocztowy=temp_user.kod_pocztowy,
            miasto=temp_user.miasto,
            telefon=temp_user.telefon,
        )
        # Usuń z tymczasowej tabeli
        temp_user.delete()
        return HttpResponse("Konto potwierdzone! Możesz się zalogować.")
    except TempUser.DoesNotExist:
        return HttpResponse("Nieprawidłowy lub wygasły link weryfikacyjny.", status=400)