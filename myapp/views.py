import csv
import io

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from myapp.models import Transaction
from mysite.predict import predict
from mysite.predict import updateDataset
from mysite.dashboard import showDashboard
from django.core.files.storage import FileSystemStorage


def home(request):
    return render(request, 'home.html')


def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged in")
            return redirect('/myapp/dashboard')
        else:
            messages.error(request, "Invalid credentials, please try again!")
            return redirect('/myapp/login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username, email, password)
        user.first_name = firstName
        user.last_name = lastName
        user.save()
        return redirect('/myapp/login')
    else:
        return render(request, 'register.html')


def logOut(request):
    logout(request)
    messages.success(request, "Successfully Logged out")
    return redirect('/myapp/')


def dashboard(request):
    return showDashboard(request, 0)


def manual(request):
    if request.method == 'POST':
        user = request.user
        date = request.POST['dateOfTransaction']
        description = request.POST['description']
        cost = request.POST['cost']
        category = request.POST['category']
        if category == "Unknown":
            category = predict(description)[0]
        elif user.username == 'admin':
            updateDataset(date, description, cost, category)

        transaction = Transaction(user=user, date=date, description=description, cost=cost, category=category)
        transaction.save()

        return redirect("/myapp/dashboard")
    else:
        return render(request, 'manual.html')


def handlePredict(request):
    if request.method == 'POST':
        transaction = request.POST['transaction']
        prediction = predict(transaction)[0]

    return HttpResponse(prediction)


def csvUpload(request):
    context = {}
    if request.method == "GET":
        return render(request, 'csvUpload.html')

    csv_file = request.FILES['file']
    dataset = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(dataset)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, transaction = Transaction.objects.update_or_create(
            user=request.user,
            date=column[1],
            description=column[2],
            cost=column[3],
            category=column[4],
        )
    fs = FileSystemStorage()
    name = fs.save(csv_file.name, csv_file)
    context['url'] = fs.url(name)

    return render(request, 'csvUpload.html', context)


def transactions(request):
    transaction = Transaction.objects.filter(user_id=request.user.id)
    return render(request, 'transactions.html', {'transactions': transaction})


def charts(request):
    total_value = showDashboard(request, 1)
    return render(request, 'charts.html', {'total_value': total_value})

