from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('create-an-account', views.register, name='register')
]
