from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import auth_user_restricted_access


@auth_user_restricted_access
def register(request):
    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'Password should be at least 6 characters')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'Password mismatch, please put same password')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Please enter a valid email address')
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'This username is taken choose another one')
            context['has_error'] = True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'This email already in used choose another one')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'authentication/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Account created successfully, now you can login')
        return redirect('login')
           
    return render(request, 'authentication/register.html')


@auth_user_restricted_access
def user_login(request):
    if request.method == "POST":
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Invalid credentials')
            return render(request, 'authentication/login.html', context)

        login(request, user)
        messages.add_message(request, messages.SUCCESS,
                             f'Welcome to Todo {user.username}')
        return redirect(reverse('home'))

    return render(request, 'authentication/login.html')


def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS,
                         'You have logged out successfully!')
    return redirect(reverse('login'))
