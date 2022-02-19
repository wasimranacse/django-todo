

from django.shortcuts import render
from django.shortcuts import render


def handle_not_found_page(request, exception):
    return render(request, 'not-found.html')


def handle_server_error(request):
    return render(request, 'server-error.html')
