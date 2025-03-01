from django.urls import path
from . import views

app_name = 'konta'
urlpatterns = [
    path('profil/', views.profil, name='profil'),
    path('edytuj/', views.edytuj_profil, name='edytuj_profil'),
    path('usun/', views.usun_konto, name='usun_konto'),
    path('check_username/', views.check_username, name='check_username'),
]