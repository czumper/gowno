from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate
from .models import UserProfile

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
    
    def save(self, request):
        user = super().save(request)
        UserProfile.objects.create(
            user=user,
            ulica=self.cleaned_data['ulica'],
            numer_domu=self.cleaned_data['numer_domu'],
            numer_mieszkania=self.cleaned_data['numer_mieszkania'],
            kod_pocztowy=self.cleaned_data['kod_pocztowy'],
            miasto=self.cleaned_data['miasto'],
            telefon=self.cleaned_data['telefon']
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
    class Meta:
        model = UserProfile
        fields = ['ulica', 'numer_domu', 'numer_mieszkania', 'kod_pocztowy', 'miasto', 'telefon']