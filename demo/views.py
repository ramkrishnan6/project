import csv
import io
import os
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from myapp.models import Transaction, Budget

from mysite.predict import predict
from mysite.predict import updateDataset
from mysite.dashboard import calculateTotal, calculateTotalWithRange, getDate, getFraction, calculateMonthlyTotal
from mysite.dashboard import showBudget
from mysite.ocr import ocr
from django.core.files.storage import FileSystemStorage
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from myapp.forms import UserUpdateForm, ProfileUpdateForm


def home(request):
    user = authenticate(username='admin', password='admin')
    login(request, user)
    categoryTotal = calculateTotal(request)["categoryTotal"]
    total = calculateTotal(request)["total"]
    isEmpty = all(total == 0 for total in categoryTotal)

    if request.method == "POST":
        if request.POST.get('setDateRange'):
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            isEmpty = all(total == 0 for total in categoryTotal)
            categoryTotal = calculateTotalWithRange(request, startDate, endDate)['categoryTotal']
            total = calculateTotalWithRange(request, startDate, endDate)['total']
            return render(request, 'demo/dashboard.html', {
                'categoryTotal': categoryTotal,
                'total': total,
                'isEmpty': isEmpty
            })
    return render(request, 'demo/dashboard.html', {
        'categoryTotal': categoryTotal,
        'total': total,
        'isEmpty': isEmpty
    })


def manual(request):
    if request.method == 'GET':
        showManualCard = True
        return render(request, 'demo/manual.html', {'showManualCard': showManualCard})

    if request.POST.get('manualAdd'):
        user = request.user
        date = request.POST['dateOfTransaction']
        description = request.POST['description']
        cost = request.POST['cost']
        category = request.POST['category']
        if category == "Unknown":
            category = predict(description)[0]
            showManualCard = False
            return render(request, 'demo/manual.html',
                          {'user': user,
                           'date': date,
                           'description': description,
                           'cost': cost,
                           'category': category,
                           'showManualCard': showManualCard
                           })
        else:
            updateDataset(description, category)
            transaction = Transaction(user=user, date=date, description=description, cost=cost, category=category)
            transaction.save()
            return redirect("/")

    if request.POST.get('confirmCategory'):
        user = request.user
        date = request.POST['dateOfTransaction']
        description = request.POST['description']
        cost = request.POST['cost']
        category = request.POST['category']
        updateDataset(description, category)
        transaction = Transaction(user=user, date=date, description=description, cost=cost, category=category)
        transaction.save()
        return redirect("/")


def handlePredict(request):
    if request.method == 'POST':
        transaction = request.POST['transaction']
        prediction = predict(transaction)[0]

    return HttpResponse(prediction)


def csvUpload(request):
    context = {}
    if request.method == "GET":
        return render(request, 'demo/csvUpload.html')

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

    return render(request, 'demo/csvUpload.html', context)


def transactions(request):
    transaction = Transaction.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        if request.POST.get('delete'):
            for transaction in transaction:
                if request.POST.get("t" + str(transaction.id)) == "clicked":
                    transaction.delete()

    transaction = Transaction.objects.filter(user_id=request.user.id)
    return render(request, 'demo/transactions.html', {'transactions': transaction})


def charts(request):
    categoryTotal = calculateTotal(request)["categoryTotal"]
    isEmpty = all(total == 0 for total in categoryTotal)

    if request.method == "POST":
        if request.POST.get('setDateRange'):
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')

            categoryTotal = calculateTotalWithRange(request, startDate, endDate)['categoryTotal']
            return render(request, 'demo/charts.html', {
                'categoryTotal': categoryTotal,
                'isEmpty': isEmpty,
            })
    return render(request, 'demo/charts.html', {
        'categoryTotal': categoryTotal,
        'isEmpty': isEmpty,
    })


def bill(request):
    if request.method == 'GET':
        showBillCard = True
        return render(request, 'demo/bill.html', {"showBillCard": showBillCard})

    elif request.method == "POST":

        if request.POST.get("bill"):

            image = request.FILES['file']
            fs = FileSystemStorage()
            file = fs.save(str(request.user.id) + '.jpeg', image)
            file_name = os.path.basename(file)
            transaction = ocr(file_name)
            category = predict(transaction[1])[0]
            showBillCard = False
            return render(request, 'demo/bill.html',
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
            updateDataset(description, category)
            return redirect("/")


class TransactionUpdateView(UserPassesTestMixin, UpdateView):
    model = Transaction
    fields = ['date', 'description', 'cost']
    template_name = 'demo/myapp/transaction_form.html'
    success_url = '/transactions'

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.user:
            return True
        return False


def profile(request):
    img = User.objects.filter(id=request.user.id).first()
    return render(request, 'demo/profile.html', {'img': img})


def ProfileUpdate(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'demo/profile_form.html', context)


class BudgetCreateView(CreateView):
    model = Budget
    fields = ['automobile', 'bank', 'cash', 'education', 'entertainment', 'fine', 'food',
              'health', 'other', 'paytm', 'recharge', 'shopping', 'travel', 'upi', 'month']
    template_name = 'demo/myapp/budget_form.html'
    success_url = '/budget'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BudgetUpdateView(UserPassesTestMixin, UpdateView):
    model = Budget
    fields = ['automobile', 'bank', 'cash', 'education', 'entertainment', 'fine', 'food',
              'health', 'other', 'paytm', 'recharge', 'shopping', 'travel', 'upi', 'month']
    template_name = 'demo/budget_update.html'
    success_url = '/budget'

    def test_func(self):
        budget = self.get_object()
        if self.request.user == budget.user:
            return True
        return False


def BudgetPage(request):
    budget = Budget.objects.filter(user_id=request.user.id)
    return render(request, 'demo/budget.html', {'budget': budget})


def analysis(request):
    month = datetime.now().month
    year = datetime.now().year
    buffer = getDate(month, year)

    startDate = buffer['startDate']
    endDate = buffer['endDate']
    charMonth = buffer['charMonth']

    buffer = showBudget(request, charMonth)
    budgetList = buffer['budgetList']

    categoryTotal = calculateTotalWithRange(request, startDate, endDate)['categoryTotal']
    buffer = getFraction(categoryTotal, budgetList, 0)
    progress = buffer["list_z"]
    colour = buffer["colour"]

    buffer = calculateMonthlyTotal(request, year)
    monthlyTotal = buffer['monthlyTotal']
    monthlyColour = buffer['colour']
    budgetTotalList = buffer['budgetTotalList']
    monthlyTotalPercentage = buffer['monthlyTotalPercentage']

    isEmpty = all(total == 0 for total in categoryTotal)

    if request.method == "POST":
        if request.POST.get('setDateRange'):
            month = request.POST.get('month')
            year = request.POST.get('year')
            buffer = getDate(month, year)

            startDate = buffer['startDate']
            endDate = buffer['endDate']
            charMonth = buffer['charMonth']

            buffer = showBudget(request, charMonth)
            budgetList = buffer['budgetList']

            categoryTotal = calculateTotalWithRange(request, startDate, endDate)['categoryTotal']
            buffer = getFraction(categoryTotal, budgetList, 0)
            progress = buffer["list_z"]
            colour = buffer["colour"]

            buffer = calculateMonthlyTotal(request, year)
            monthlyTotal = buffer['monthlyTotal']
            monthlyColour = buffer['colour']
            budgetTotalList = buffer['budgetTotalList']
            monthlyTotalPercentage = buffer['monthlyTotalPercentage']

            isEmpty = all(total == 0 for total in categoryTotal)

            return render(request, 'demo/analysis.html', {
                'categoryTotal': categoryTotal,
                'isEmpty': isEmpty,
                'budgetList': budgetList,
                'charMonth': charMonth,
                'year': year,
                'progress': progress,
                'colour': colour,
                'monthlyTotal': monthlyTotal,
                'monthlyColour': monthlyColour,
                'budgetTotalList': budgetTotalList,
                'monthlyTotalPercentage': monthlyTotalPercentage
            })
    return render(request, 'demo/analysis.html', {
        'categoryTotal': categoryTotal,
        'isEmpty': isEmpty,
        'budgetList': budgetList,
        'charMonth': charMonth,
        'year': year,
        'progress': progress,
        'colour': colour,
        'monthlyTotal': monthlyTotal,
        'monthlyColour': monthlyColour,
        'budgetTotalList': budgetTotalList,
        'monthlyTotalPercentage': monthlyTotalPercentage
    })
