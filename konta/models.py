from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ulica = models.CharField(max_length=40)
    numer_domu = models.CharField(max_length=5)
    numer_mieszkania = models.CharField(max_length=5, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=6)
    miasto = models.CharField(max_length=40)
    telefon = models.CharField(max_length=9)

    def __str__(self):
        return self.user.username