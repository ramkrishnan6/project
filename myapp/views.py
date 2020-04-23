from django.contrib import messages
from django.http.response import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from myapp.models import Transaction
from mysite.predict import predict


def home(request):
    return render(request, 'home.html')


def logIn(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def dashboard(request):
    transactions_automobile = Transaction.objects.filter(user_id=request.user.id, category="Automobile")
    total_automobile = 0
    for transaction in transactions_automobile:
        total_automobile = total_automobile + transaction.cost

    transactions_bank = Transaction.objects.filter(user_id=request.user.id, category="Bank Transfer")
    total_bank = 0
    for transaction in transactions_bank:
        total_bank = total_bank + transaction.cost

    transactions_cash = Transaction.objects.filter(user_id=request.user.id, category="Cash Withdrawal")
    total_cash = 0
    for transaction in transactions_cash:
        total_cash = total_cash + transaction.cost

    transactions_education = Transaction.objects.filter(user_id=request.user.id, category="Education")
    total_education = 0
    for transaction in transactions_education:
        total_education = total_education + transaction.cost

    transactions_entertainment = Transaction.objects.filter(user_id=request.user.id, category="Entertainment")
    total_entertainment = 0
    for transaction in transactions_entertainment:
        total_entertainment = total_entertainment + transaction.cost

    transactions_fine = Transaction.objects.filter(user_id=request.user.id, category="Fine")
    total_fine = 0
    for transaction in transactions_fine:
        total_fine = total_fine + transaction.cost

    transactions_food = Transaction.objects.filter(user_id=request.user.id, category="Food")
    total_food = 0
    for transaction in transactions_food:
        total_food = total_food + transaction.cost

    transactions_health = Transaction.objects.filter(user_id=request.user.id, category="Health Care")
    total_health = 0
    for transaction in transactions_health:
        total_health = total_health + transaction.cost
#TODO - EXCHANGE IGNORE WITH OTHER
    transactions_ignore = Transaction.objects.filter(user_id=request.user.id, category="Ignore")
    total_ignore = 0
    for transaction in transactions_ignore:
        total_ignore = total_ignore + transaction.cost

    transactions_paytm = Transaction.objects.filter(user_id=request.user.id, category="Paytm")
    total_paytm = 0
    for transaction in transactions_paytm:
        total_paytm = total_paytm + transaction.cost

    transactions_shopping = Transaction.objects.filter(user_id=request.user.id, category="Shopping")
    total_shopping = 0
    for transaction in transactions_shopping:
        total_shopping = total_shopping + transaction.cost

    transactions_travel = Transaction.objects.filter(user_id=request.user.id, category="Travel")
    total_travel = 0
    for transaction in transactions_travel:
        total_travel = total_travel + transaction.cost

    transactions_upi = Transaction.objects.filter(user_id=request.user.id, category="UPI")
    total_upi = 0
    for transaction in transactions_upi:
        total_upi = total_upi + transaction.cost

    transactions_recharge = Transaction.objects.filter(user_id=request.user.id, category="Recharge")
    total_recharge = 0
    for transaction in transactions_recharge:
        total_recharge = total_recharge + transaction.cost

    transactions = Transaction.objects.filter(user_id=request.user.id)
    total = 0
    for transaction in transactions:
        total = total + transaction.cost

    total_value = [total_automobile, total_bank, total_cash, total_education,
                   total_entertainment, total_fine, total_food, total_health,
                   total_ignore, total_paytm, total_shopping, total_travel,
                   total_upi, total_recharge]

    categories = ['Automobile', 'Bank Transfer', 'Cash Withdrawal', 'Education',
                  'Entertainment', 'Fine', 'Food', 'Health Care',
                   'Ignore', 'PayTM', 'Shopping', 'Travel',
                   'UPI', 'Recharge']

    return render(request, 'dashboard.html', {
        'total_automobile': total_automobile,
        'total_bank' : total_bank,
        'total_cash': total_cash,
        'total_education': total_education,
        'total_entertainment': total_entertainment,
        'total_fine': total_fine,
        'total_food': total_food,
        'total_health': total_health,
        'total_ignore': total_ignore,
        'total_paytm': total_paytm,
        'total_shopping': total_shopping,
        'total_travel': total_travel,
        'total_upi': total_upi,
        'total_recharge': total_recharge,
        'total': total,
        'total_value': total_value,
        'transactions': transactions,
        'categories': categories,

    })


def manual(request):
    return render(request, 'manual.html')


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


def handlePredict(request):
    if request.method == 'POST':
        transaction = request.POST['transaction']
    else:
        return HttpResponseNotFound('<h1>Error 404 - Page not found</h1>')
    prediction = predict(transaction)[0]
    return render(request, 'dashboard.html', {'prediction': prediction})
    #return HttpResponse(prediction)


def manualAdd(request):
    if request.method == 'POST':
        user = request.user
        date = request.POST['dateOfTransaction']
        description = request.POST['description']
        cost = request.POST['cost']
        category = request.POST['category']

        if category == "Unknown":
            category = predict(description)[0]

        transaction = Transaction(user=user, date=date, description=description, cost=cost, category=category)
        transaction.save()

    else:
        return HttpResponseNotFound('<h1>Error 404 - Page not found</h1>')
    return redirect("/myapp/dashboard")


def index(request):
    return render(request, 'index.html')