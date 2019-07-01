from django.urls import path
from .views import fehlertest


urlpatterns = [
    path('fehlertest/', fehlertest, name='pruefungen-fehlertest'),
]