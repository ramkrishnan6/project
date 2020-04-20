from django.contrib import messages
from django.http.response import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'home.html')


def logIn(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def handleSignup(request):
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstName
        myuser.last_name = lastName
        myuser.save()
        return redirect('login')
    else:
        return HttpResponseNotFound('<h1>Error 404 - Page not found</h1>')


def handleSignin(request):
    if request.method == 'POST':
        loginUsername = request.POST['loginUsername']
        loginPassword = request.POST['loginPassword']

        user = authenticate(username=loginUsername, password=loginPassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials, please try again!")
            return redirect('login')
    else:
        return HttpResponseNotFound('<h1>Error 404 - Page not found</h1>')


def handleSignout(request):
    logout(request)
    messages.success(request, "Successfully Logged out")
    return redirect('login')
