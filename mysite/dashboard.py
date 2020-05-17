from myapp.models import Transaction
from myapp.models import Budget


def calculateTotal(request):

    categories = ["Automobile", "Bank Transfer", "Cash Withdrawal", "Education", "Entertainment", "Fine",
                  "Food", "Health Care", "Other", "Paytm", "Recharge", "Shopping", "Travel", "UPI"]
    categoryTotal = [0] * 14

    for index, x in enumerate(categories):
        transaction_all = Transaction.objects.filter(user_id=request.user.id, category=x)
        for transaction in transaction_all:
            categoryTotal[index] = categoryTotal[index] + transaction.cost

    total = sum(categoryTotal)

    return {
        'categoryTotal': categoryTotal,
        'total': total,
    }


def showBudget(request):
    budgetValues = Budget.objects.filter(user_id=request.user.id)
    budgetList = [0] * 14
    for x in budgetValues:
        budgetList = [x.automobile, x.bank, x.cash, x.education, x.entertainment, x.food, x.fine,
                      x.health, x.other, x.paytm, x.recharge, x.shopping, x.travel, x.upi]

    return budgetList
