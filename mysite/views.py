# I have created this file
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse("<h1>Home Page</h1>")


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')
