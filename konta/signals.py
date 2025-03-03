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
    try:
        temp_user = TempUser.objects.get(email=email_address.email)
        user = User.objects.get(email=email_address.email)
        UserProfile.objects.create(
            user=user,
            ulica=temp_user.ulica,
            numer_domu=temp_user.numer_domu,
            numer_mieszkania=temp_user.numer_mieszkania,
            kod_pocztowy=temp_user.kod_pocztowy,
            miasto=temp_user.miasto,
            telefon=temp_user.telefon,
        )
        user.is_active = True  # Aktywuj użytkownika po weryfikacji
        user.save()
        temp_user.delete()
    except TempUser.DoesNotExist:
        pass  # Jeśli nie ma w TempUser, to już zweryfikowany użytkownik