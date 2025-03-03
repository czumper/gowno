from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TempUser(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Przechowamy zahashowane hasło
    ulica = models.CharField(max_length=100)
    numer_domu = models.CharField(max_length=10)
    numer_mieszkania = models.CharField(max_length=10, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=6)
    miasto = models.CharField(max_length=50)
    telefon = models.CharField(max_length=12)  # +48 i 9 cyfr
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ulica = models.CharField(max_length=40)
    numer_domu = models.CharField(max_length=5)
    numer_mieszkania = models.CharField(max_length=5, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=6)
    miasto = models.CharField(max_length=40)
    telefon = models.CharField(max_length=13)

    def __str__(self):
        return self.user.username