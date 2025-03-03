from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from allauth.account.signals import password_changed, email_confirmed
from django.conf import settings
from django.contrib import messages
from .models import TempUser, UserProfile
from django.contrib.auth import get_user_model

@receiver(password_changed)
def send_password_change_confirmation(sender, request, user, **kwargs):
    subject = "Pitcernia: Potwierdzenie zmiany hasła"
    message = f"Cześć {user.username}!\n\nTwoje hasło w Pitcerni zostało pomyślnie zmienione.\n\nSmacznego!\nEkipa Pitcerni 🍕"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    messages.success(request, "Hasło zmienione pomyślnie!", extra_tags="password_changed")

User = get_user_model()

@receiver(email_confirmed)
def handle_email_confirmed(sender, request, email_address, **kwargs):
    profile_data = request.session.get('profile_data', {})
    if profile_data and profile_data.get('email') == email_address.email:
        user = User.objects.get(email=email_address.email)
        UserProfile.objects.create(
            user=user,
            ulica=profile_data['ulica'],
            numer_domu=profile_data['numer_domu'],
            numer_mieszkania=profile_data.get('numer_mieszkania', ''),
            kod_pocztowy=profile_data['kod_pocztowy'],
            miasto=profile_data['miasto'],
            telefon=profile_data['telefon'],
        )
        del request.session['profile_data']