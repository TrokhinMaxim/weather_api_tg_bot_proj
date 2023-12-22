from django.urls import path
from .views import weather, mainpage

urlpatterns = [
    path("", mainpage, name="mainpage"),
    path("weather/<str:city_name>/", weather, name="weather"),
]
