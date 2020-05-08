import csv
import io
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from myapp.models import Transaction
from mysite.predict import predict
from mysite.predict import updateDataset
from mysite.dashboard import showDashboard
from mysite.ocr import ocr
from django.core.files.storage import FileSystemStorage
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin


def home(request):
    return render(request, 'home.html')


def logIn(request):
    if request.method == 'POST':
        username = request.POST['username'].replace(" ", "")
        password = request.POST['password'].replace(" ", "")
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
        firstName = request.POST['firstName'].replace(" ", "")
        lastName = request.POST['lastName'].replace(" ", "")
        username = request.POST['username'].replace(" ", "")
        email = request.POST['email'].replace(" ", "")
        password = request.POST['password'].replace(" ", "")

        user = User.objects.create_user(username, email, password)
        user.first_name = firstName
        user.last_name = lastName
        user.save()
        return redirect('/myapp/login')
    else:
        return render(request, 'register.html')


def validate_username(request):
    username = request.GET.get('username', None).replace(" ", "")
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


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
        else:
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
    if request.method == "POST":
        if request.POST.get('delete'):
            for transaction in transaction:
                if request.POST.get("t" + str(transaction.id)) == "clicked":
                    transaction.delete()

    transaction = Transaction.objects.filter(user_id=request.user.id)
    return render(request, 'transactions.html', {'transactions': transaction})


def charts(request):
    total_value = showDashboard(request, 1)
    return render(request, 'charts.html', {'total_value': total_value})


def bill(request):
    if request.method == 'GET':
        showBillCard = True
        return render(request, 'bill.html', {"showBillCard": showBillCard})

    elif request.method == "POST":

        if request.POST.get("bill"):

            image = request.FILES['file']
            fs = FileSystemStorage()
            file = fs.save(str(request.user.id) + '.jpeg', image)
            file_name = os.path.basename(file)
            transaction = ocr(file_name)
            category = predict(transaction[1])[0]
            # transaction = ['2019-05-07', "petrol", 700]
            # category = "Travel"
            showBillCard = False
            return render(request, 'bill.html',
                          {"transaction": transaction, "category": category, "showBillCard": showBillCard}
                          )

        elif request.POST.get("check"):
            user = request.user
            date = request.POST['dateOfTransaction']
            description = request.POST['description']
            cost = request.POST['cost']
            category = request.POST['category']
            transaction = Transaction(user=user, date=date, description=description, cost=cost, category=category)
            transaction.save()
            updateDataset(date, description, cost, category)
            return redirect("/myapp/dashboard")


class TransactionUpdateView(UserPassesTestMixin, UpdateView):
    model = Transaction
    fields = ['date', 'description', 'cost']
    success_url = '/myapp/transactions'

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.user:
            return True
        return False
