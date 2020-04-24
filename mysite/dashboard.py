from django.shortcuts import render

from myapp.models import Transaction


def showDashboard(request):
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

    transactions_other = Transaction.objects.filter(user_id=request.user.id, category="Other")
    total_other = 0
    for transaction in transactions_other:
        total_other = total_other + transaction.cost

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
                   total_other, total_paytm, total_shopping, total_travel,
                   total_upi, total_recharge]

    categories = ['Automobile', 'Bank Transfer', 'Cash Withdrawal', 'Education',
                  'Entertainment', 'Fine', 'Food', 'Health Care',
                  'Other', 'PayTM', 'Shopping', 'Travel',
                  'UPI', 'Recharge']

    return render(request, 'dashboard.html', {
        'total_automobile': total_automobile,
        'total_bank': total_bank,
        'total_cash': total_cash,
        'total_education': total_education,
        'total_entertainment': total_entertainment,
        'total_fine': total_fine,
        'total_food': total_food,
        'total_health': total_health,
        'total_other': total_other,
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
