from django.urls import path

from . import views

app_name = "apka"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetaleView.as_view(), name="detale"),
    path("<int:pk>/", views.WynikiView.as_view(), name="wyniki"),
    path("<int:pytanie_id>/glos/", views.glos, name="glos"),
]