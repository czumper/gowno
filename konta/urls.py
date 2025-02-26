from django.urls import path
from . import views

app_name = 'konta'
urlpatterns = [
    path('profil/', views.profil, name='profil'),
]