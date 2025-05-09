from django import forms
from allauth.account.forms import SignupForm, LoginForm, AddEmailForm
from django.contrib.auth import authenticate
import logging
from django.contrib.auth.models import User
from .models import UserProfile
from allauth.account.models import EmailAddress

COUNTRY_CODES = [
    ('+48', '+48 (Polska)'),
    ('+44', '+44 (Wielka Brytania)'),
    ('+49', '+49 (Niemcy)'),
    ('+33', '+33 (Francja)'),
]

class CustomZarejestrujForm(SignupForm):
    username = forms.CharField(max_length=20, label='Nazwa użytkownika')
    ulica = forms.CharField(max_length=40, label='Ulica')
    numer_domu = forms.CharField(max_length=5, label='Numer domu')
    numer_mieszkania = forms.CharField(max_length=5, label='Numer mieszkania', required=False)
    kod_pocztowy = forms.CharField(max_length=6, label='Kod pocztowy')
    miasto = forms.CharField(max_length=40, label='Miasto')
    phone_country_code = forms.ChoiceField(choices=COUNTRY_CODES, label='Kierunkowy', initial='+48')
    telefon = forms.CharField(max_length=9, label='Telefon')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if '@' in username:
            raise forms.ValidationError('Zabroniony znak')
        return username
    
    def clean_telefon(self):
        telefon = self.cleaned_data['telefon']
        if not telefon.isdigit() or len(telefon) != 9:
            raise forms.ValidationError('Numer telefonu musi mieć dokładnie 9 cyfr.')
        return telefon
    
    def save(self, request):
        user = super().save(request)
        calytelefon = f"{self.cleaned_data['phone_country_code']}{self.cleaned_data['telefon']}"
        UserProfile.objects.create(
            user=user,
            ulica=self.cleaned_data['ulica'],
            numer_domu=self.cleaned_data['numer_domu'],
            numer_mieszkania=self.cleaned_data['numer_mieszkania'],
            kod_pocztowy=self.cleaned_data['kod_pocztowy'],
            miasto=self.cleaned_data['miasto'],
            telefon=calytelefon,
        )
        return user

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
                user = authenticate(request=self.request, email=login, password=password)
            else:
                user = authenticate(request=self.request, username=login, password=password)
            if user is None:
                raise forms.ValidationError('Niepoprawne dane logowania')
            self.user = user
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    phone_country_code = forms.ChoiceField(choices=COUNTRY_CODES, label='Kierunkowy', required=False)
    telefon = forms.CharField(max_length=9, label='Telefon')

    class Meta:
        model = UserProfile
        fields = ['ulica', 'numer_domu', 'numer_mieszkania', 'kod_pocztowy', 'miasto', 'telefon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.telefon:
            # Rozdzielamy telefon na kierunkowy i numer
            if self.instance.telefon.startswith('+'):
                self.initial['phone_country_code'] = self.instance.telefon[:3]  # np. +48
                self.initial['telefon'] = self.instance.telefon[3:]  # reszta numeru
            else:
                self.initial['telefon'] = self.instance.telefon

    def clean_telefon(self):
        telefon = self.cleaned_data['telefon']
        if not telefon.isdigit() or len(telefon) != 9:
            raise forms.ValidationError('Numer telefonu musi mieć dokładnie 9 cyfr.')
        return telefon

    def save(self, commit=True):
        instance = super().save(commit=False)
        full_phone = f"{self.cleaned_data['phone_country_code']}{self.cleaned_data['telefon']}"
        instance.telefon = full_phone
        if commit:
            instance.save()
        return instance
    
class CustomAddEmailForm(AddEmailForm):
    password = forms.CharField(label="Aktualne hasło", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if EmailAddress.objects.filter(email=email).exclude(user=self.user).exists():
            raise forms.ValidationError("Ten adres email jest już zajęty przez inne konto.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        email = cleaned_data.get('email')

        if password and email:
            if not self.user.check_password(password):
                raise forms.ValidationError("Podane hasło jest nieprawidłowe.")
        return cleaned_data