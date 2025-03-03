from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, get_user_model
from .models import UserProfile, TempUser
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
import uuid

COUNTRY_CODES = [
    ('+48', '+48 (Polska)'),
    ('+49', '+49 (Niemcy)'),    
    ('+44', '+44 (Wielka Brytania)'),
]

class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, label='Nazwa użytkownika', required=True)
    email = forms.EmailField(label='Email', required=True)
    ulica = forms.CharField(max_length=100, label='Ulica', required=True)
    numer_domu = forms.CharField(max_length=10, label='Numer domu', required=True)
    numer_mieszkania = forms.CharField(max_length=10, label='Numer mieszkania', required=False)
    kod_pocztowy = forms.CharField(max_length=6, label='Kod pocztowy', required=True)
    miasto = forms.CharField(max_length=50, label='Miejscowość', required=True)
    phone_country_code = forms.ChoiceField(choices=COUNTRY_CODES, label='Kierunkowy', initial='+48', required=True)
    telefon = forms.CharField(max_length=9, label='Numer telefonu', required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if '@' in username:
            raise forms.ValidationError("Nazwa użytkownika nie może zawierać znaku '@'.")
        if User.objects.filter(username=username).exists() or TempUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Ta nazwa użytkownika jest już zajęta.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if User.objects.filter(email=email).exists() or TempUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten email jest już zajęty.")
        return email

    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon', '')
        if not telefon.isdigit() or len(telefon) != 9:
            raise forms.ValidationError("Numer telefonu musi mieć dokładnie 9 cyfr.")
        return telefon

    def clean_kod_pocztowy(self):
        kod_pocztowy = self.cleaned_data.get('kod_pocztowy', '')
        if not kod_pocztowy[:2].isdigit() or not kod_pocztowy[3:].isdigit() or kod_pocztowy[2] != '-' or len(kod_pocztowy) != 6:
            raise forms.ValidationError("Kod pocztowy musi być w formacie XX-XXX (np. 12-345).")
        return kod_pocztowy
    

    def save(self, request):
        temp_user = TempUser(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=make_password(self.cleaned_data['password1']),
            ulica=self.cleaned_data['ulica'],
            numer_domu=self.cleaned_data['numer_domu'],
            numer_mieszkania=self.cleaned_data.get('numer_mieszkania', ''),
            kod_pocztowy=self.cleaned_data['kod_pocztowy'],
            miasto=self.cleaned_data['miasto'],
            telefon=f"{self.cleaned_data['phone_country_code']}{self.cleaned_data['telefon']}",
        )
        temp_user.save()
        # Zapisz użytkownika w allauth, ale bez profilu – profil dodamy po weryfikacji
        user = super().save(request)
        user.is_active = False  # Wyłączamy użytkownika do weryfikacji
        user.save()
        return user
"""
class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, label='Nazwa użytkownika')
    ulica = forms.CharField(max_length=100, label='Ulica')
    numer_domu = forms.CharField(max_length=10, label='Numer domu')
    numer_mieszkania = forms.CharField(max_length=10, label='Numer mieszkania', required=False)
    kod_pocztowy = forms.CharField(max_length=6, label='Kod pocztowy')
    miasto = forms.CharField(max_length=50, label='Miejscowość')
    phone_country_code = forms.ChoiceField(choices=COUNTRY_CODES, label='Kierunkowy', initial='+48')
    telefon = forms.CharField(max_length=9, label='Numer telefonu')

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if '@' in username:
            raise forms.ValidationError("Nazwa użytkownika nie może zawierać znaku '@'.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten email jest już zajęty.")
        return email

    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon', '')
        if not telefon.isdigit() or len(telefon) != 9:
            raise forms.ValidationError("Numer telefonu musi mieć dokładnie 9 cyfr.")
        return telefon

    def clean_kod_pocztowy(self):
        kod_pocztowy = self.cleaned_data.get('kod_pocztowy', '')
        if not kod_pocztowy[:2].isdigit() or not kod_pocztowy[3:].isdigit() or kod_pocztowy[2] != '-' or len(kod_pocztowy) != 6:
            raise forms.ValidationError("Kod pocztowy musi być w formacie XX-XXX (np. 12-345).")
        return kod_pocztowy

    def signup(self, request, user):
        UserProfile.objects.create(
            user=user,
            ulica=self.cleaned_data['ulica'],
            numer_domu=self.cleaned_data['numer_domu'],
            numer_mieszkania=self.cleaned_data.get('numer_mieszkania', ''),
            kod_pocztowy=self.cleaned_data['kod_pocztowy'],
            miasto=self.cleaned_data['miasto'],
            telefon=f"{self.cleaned_data['phone_country_code']}{self.cleaned_data['telefon']}",
        )
"""
        

class CustomLogowanieForm(LoginForm):
    login = forms.CharField(max_length=20, label='Nazwa użytkownika lub email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields ['login']
        self.fields['login'] = forms.CharField(max_length=50, label='Nazwa użytkownika lub email')

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if login and password:
            if '@' in login:
                self.user = authenticate(request=self.request, email=login, password=password)
            else:
                self.user = authenticate(request=self.request, username=login, password=password)
            if self.user is None:
                raise forms.ValidationError("Błędna nazwa użytkownika/email lub hasło.")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    phone_country_code = forms.ChoiceField(choices=COUNTRY_CODES, label='Kierunkowy', required=False)
    telefon = forms.CharField(max_length=9, label='Numer telefonu', required=False)

    class Meta:
        model = UserProfile
        fields = ['ulica', 'numer_domu', 'numer_mieszkania', 'kod_pocztowy', 'miasto', 'telefon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.telefon:
            if self.instance.telefon.startswith('+48'):
                self.initial['phone_country_code'] = '+48'
                self.initial['telefon'] = self.instance.telefon[3:]
            elif self.instance.telefon.startswith('+49'):
                self.initial['phone_country_code'] = '+49'
                self.initial['telefon'] = self.instance.telefon[3:]
            elif self.instance.telefon.startswith('+44'):
                self.initial['phone_country_code'] = '+44'
                self.initial['telefon'] = self.instance.telefon[3:]
            elif self.instance.telefon.startswith('+33'):
                self.initial['phone_country_code'] = '+33'
                self.initial['telefon'] = self.instance.telefon[3:]

    def clean_telefon(self):
        telefon = self.cleaned_data['telefon']
        if telefon and (not telefon.isdigit() or len(telefon) != 9):
            raise forms.ValidationError("Numer telefonu musi mieć dokładnie 9 cyfr.")
        return telefon

    def clean_kod_pocztowy(self):
        kod_pocztowy = self.cleaned_data['kod_pocztowy']
        if not kod_pocztowy[:2].isdigit() or not kod_pocztowy[3:].isdigit() or kod_pocztowy[2] != '-' or len(kod_pocztowy) != 6:
            raise forms.ValidationError("Kod pocztowy musi być w formacie XX-XXX (np. 12-345).")
        return kod_pocztowy

    def save(self, commit=True):
        instance = super().save(commit=False)
        phone_country_code = self.cleaned_data.get('phone_country_code', '+48')
        telefon = self.cleaned_data['telefon']
        if telefon:
            instance.telefon = f"{phone_country_code}{telefon}"
        if commit:
            instance.save()
        return instance