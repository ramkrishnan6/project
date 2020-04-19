# I have created this file
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def home(request):
    return HttpResponse("<h1>Home Page</h1>")


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def dashboard(request):
    return HttpResponse("<h1>Your Dashboard</h1>")


def handleSignup(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']

        myuser = User.objects.create_user(username, email, password)
        myuser.name = name
        myuser.save()
        return redirect('dashboard')
    else:
        return HttpResponse('404 - Not Found')


