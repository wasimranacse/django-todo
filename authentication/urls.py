from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('activate-user/<uidb64>/<token>', views.user_email_activation, name='activate'),
]
