from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from allauth.account.signals import password_changed
from django.conf import settings
from django.contrib import messages

@receiver(password_changed)
def send_password_change_confirmation(sender, request, user, **kwargs):
    subject = "Pitcernia: Potwierdzenie zmiany hasła"
    message = f"Cześć {user.username}!\n\nTwoje hasło w Pitcerni zostało pomyślnie zmienione.\n\nSmacznego!\nEkipa Pitcerni 🍕"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    messages.success(request, "Hasło zmienione pomyślnie!", extra_tags="password_changed")