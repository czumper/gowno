from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate
from .models import UserProfile

COUNTRY_CODES = [
    ('+48', '+48 (Polska)'),
    ('+49', '+49 (Niemcy)'),    
    ('+44', '+44 (Wielka Brytania)'),
    ('+33', '+33 (Francja)'),
    ('+34', '+34 (Hiszpania)'),
    ('+39', '+39 (Włochy)'),
    ('+31', '+31 (Holandia)'),
    ('+32', '+32 (Belgia)'),
    ('+41', '+41 (Szwajcaria)'),
    ('+43', '+43 (Austria)'),
    ('+420', '+420 (Czechy)'),
    ('+421', '+421 (Słowacja)'),
    ('+386', '+386 (Słowenia)'),
    ('+385', '+385 (Chorwacja)'),
    ('+387', '+387 (Bośnia i Hercegowina)'),
    ('+381', '+381 (Serbia)'),
    ('+382', '+382 (Czarnogóra)'),
    ('+383', '+383 (Kosowo)'),
    ('+386', '+386 (Macedonia)'),
    ('+355', '+355 (Albania)'),
    ('+30', '+30 (Grecja)'),
    ('+90', '+90 (Turcja)'),
    ('+7', '+7 (Rosja)'),
    ('+380', '+380 (Ukraina)'),
    ('+373', '+373 (Mołdawia)'),
    ('+375', '+375 (Białoruś)'),
    ('+370', '+370 (Litwa)'),
    ('+371', '+371 (Łotwa)'),
    ('+372', '+372 (Estonia)'),
    ('+358', '+358 (Finlandia)'),
    ('+46', '+46 (Szwecja)'),
    ('+47', '+47 (Norwegia)'),
    ('+358', '+358 (Finlandia)'),
    ('+354', '+354 (Islandia)'),
    ('+353', '+353 (Irlandia)'),
    ('+41', '+41 (Liechtenstein)'),
    ('+43', '+43 (Luksemburg)'),
    ('+377', '+377 (Monako)'),
    ('+377', '+377 (Andora)'),
    ('+376', '+376 (San Marino)'),
    ('+378', '+378 (Watykan)'),
    ('+1', '+1 (USA)'),
    ('+1', '+1 (Kanada)'),
    ('+52', '+52 (Meksyk)'),
]

class CustomZarejestrujForm(SignupForm):
    username = forms.CharField(max_length=20, label='Nazwa użytkownika')
    ulica = forms.CharField(max_length=40, label='Ulica')
    numer_domu = forms.CharField(max_length=5, label='Numer domu')
    numer_mieszkania = forms.CharField(max_length=5, label='Numer mieszkania', required=False)
    kod_pocztowy = forms.CharField(max_length=6, label='Kod pocztowy')
    miasto = forms.CharField(max_length=40, label='Miasto')
    telefon = forms.CharField(max_length=9, label='Telefon')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if '@' in username:
            raise forms.ValidationError('Zabroniony znak')
        return username
    
    def clean_telefon(self):
        telefon = self.cleaned_data['telefon']
        if not telefon.isdigit() or len(telefon) != 9:
            raise forms.ValidationError("Numer telefonu musi mieć dokładnie 9 cyfr.")
        return telefon

    def clean_kod_pocztowy(self):
        kod_pocztowy = self.cleaned_data['kod_pocztowy']
        if not kod_pocztowy[:2].isdigit() or not kod_pocztowy[3:].isdigit() or kod_pocztowy[2] != '-' or len(kod_pocztowy) != 6:
            raise forms.ValidationError("Kod pocztowy musi być w formacie XX-XXX (np. 69-420).")
        return kod_pocztowy
    
    def save(self, request):
        user = super().save(request)
        UserProfile.objects.create(
            user=user,
            ulica=self.cleaned_data['ulica'],
            numer_domu=self.cleaned_data['numer_domu'],
            numer_mieszkania=self.cleaned_data['numer_mieszkania'],
            kod_pocztowy=self.cleaned_data['kod_pocztowy'],
            miasto=self.cleaned_data['miasto'],
            telefon=f"{self.cleaned_data['phone_country_code']}{self.cleaned_data['telefon']}",
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
                self.user = authenticate(request=self.request, email=login, password=password)
            else:
                self.user = authenticate(request=self.request, username=login, password=password)
            if self.user is None:
                raise forms.ValidationError("Błędna nazwa użytkownika/email lub hasło.")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['ulica', 'numer_domu', 'numer_mieszkania', 'kod_pocztowy', 'miasto', 'telefon']