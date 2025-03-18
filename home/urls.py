from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]

from django.urls import path
from .views import example_view

urlpatterns = [
    path('api/example/', example_view),
]
