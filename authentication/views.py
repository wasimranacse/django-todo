from multiprocessing import context
from tkinter.messagebox import NO
from django.shortcuts import redirect, render
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import auth_user_restricted_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_tokens
from django.core.mail import EmailMessage
from django.conf import settings


def send_activation_email_to_user(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_tokens.make_token(user)
    })

    email = EmailMessage(subject=email_subject, 
                        body=email_body, 
                        from_email = settings.EMAIL_FROM_USER, 
                        to=[user.email]
    ) 
    email.send()

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

        send_activation_email_to_user(user, request)

        messages.add_message(request, messages.SUCCESS,
                             'Verification email sent to your inbox, please verify and back to login')
        return redirect('login')
           
    return render(request, 'authentication/register.html')


@auth_user_restricted_access
def user_login(request):
    if request.method == "POST":
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and not user.is_email_verified:
            messages.add_message(request, messages.ERROR,
                                 'Email is not verified, please check your email inbox also the span folder')
            return render(request, 'authentication/login.html', context)

        
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


def user_email_activation(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_tokens.check_token(user, token):
        user.is_email_verified=True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'You have verified email, now you can login')
        return redirect(reverse('login'))
    
    return render(request, 'authentication/activation-failed.html', {
        'user': user,
    })
