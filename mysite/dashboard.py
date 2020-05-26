from myapp.models import Transaction
from myapp.models import Budget


# get total of each category and the total of all categories of ALL TRANSACTIONS
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


# get total of each category and the total of all categories of transactions in a given range of days
def calculateTotalWithRange(request, startDate, endDate):
    categories = ["Automobile", "Bank Transfer", "Cash Withdrawal", "Education", "Entertainment", "Fine",
                  "Food", "Health Care", "Other", "Paytm", "Recharge", "Shopping", "Travel", "UPI"]
    categoryTotal = [0] * 14

    for index, x in enumerate(categories):
        transaction_all = Transaction.objects.filter(user_id=request.user.id, category=x,
                                                     date__range=[startDate, endDate])
        for transaction in transaction_all:
            categoryTotal[index] = categoryTotal[index] + transaction.cost

    total = sum(categoryTotal)

    return {
        'categoryTotal': categoryTotal,
        'total': total,
    }


# get budget value and total of the values of a particular month
def showBudget(request, month):
    budgetValues = Budget.objects.filter(user_id=request.user.id, month=month)
    budgetList = [0] * 14

    for index, x in enumerate(budgetValues):
        budgetList = [x.automobile, x.bank, x.cash, x.education, x.entertainment, x.fine, x.food,
                      x.health, x.other, x.paytm, x.recharge, x.shopping, x.travel, x.upi]
    budgetTotal = (x.automobile + x.bank + x.cash + x.education + x.entertainment + x.fine + x.food + x.health + x.other + x.paytm + x.recharge + x.shopping + x.travel + x.upi)
    budgetTotal = int(budgetTotal)

    return {'budgetList': budgetList, 'budgetTotal': budgetTotal}


# get MONTH-WISE total of each category of TRANSACTIONS, corresponding BUDGET VALUE, COLOUR (in terms of bootstrap),
# and percentage of a given year
def calculateMonthlyTotal(request, year):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthlyTotal = [0] * 12
    budgetTotalList = [0] * 12

    for index, x in enumerate(months):
        buffer = getDate(x, year)
        startDate = buffer['startDate']
        endDate = buffer['endDate']
        budgetTotalList[index] = showBudget(request, x)["budgetTotal"]

        transaction_all = Transaction.objects.filter(user_id=request.user.id, date__range=[startDate, endDate])
        for transaction in transaction_all:
            monthlyTotal[index] = monthlyTotal[index] + transaction.cost

    buffer = getFraction(monthlyTotal, budgetTotalList, 1)
    colour = buffer['colour']
    monthlyTotalPercentage = buffer['list_z']

    return {'monthlyTotal': monthlyTotal, 'colour': colour, 'budgetTotalList': budgetTotalList,
            'monthlyTotalPercentage': monthlyTotalPercentage}


# get start date and end date of given month and year
def getDate(month, year):
    startDate = ''
    endDate = ''
    charMonth = ''

    if month == 'Jan' or month == 1:
        startDate = '{}-01-1'.format(year)
        endDate = '{}-01-31'.format(year)
        charMonth = 'Jan'
    elif month == 'Feb' or month == 2:
        startDate = '{}-02-01'.format(year)
        endDate = '{}-02-28'.format(year)
        charMonth = 'Feb'
    elif month == 'Mar' or month == 3:
        startDate = '{}-03-01'.format(year)
        endDate = '{}-03-31'.format(year)
        charMonth = 'Mar'
    elif month == 'Apr' or month == 4:
        startDate = '{}-04-01'.format(year)
        endDate = '{}-04-30'.format(year)
        charMonth = 'Apr'
    elif month == 'May' or month == 5:
        startDate = '{}-05-01'.format(year)
        endDate = '{}-05-31'.format(year)
        charMonth = 'May'
    elif month == 'Jun' or month == 6:
        startDate = '{}-06-01'.format(year)
        endDate = '{}-06-30'.format(year)
        charMonth = 'Jun'
    elif month == 'Jul' or month == 7:
        startDate = '{}-07-01'.format(year)
        endDate = '{}-07-31'.format(year)
        charMonth = 'Jul'
    elif month == 'Aug' or month == 8:
        startDate = '{}-08-01'.format(year)
        endDate = '{}-08-31'.format(year)
        charMonth = 'Aug'
    elif month == 'Sep' or month == 9:
        startDate = '{}-09-01'.format(year)
        endDate = '{}-09-30'.format(year)
        charMonth = 'Sep'
    elif month == 'Oct' or month == 10:
        startDate = '{}-10-01'.format(year)
        endDate = '{}-10-31'.format(year)
        charMonth = 'Oct'
    elif month == 'Nov' or month == 11:
        startDate = '{}-11-01'.format(year)
        endDate = '{}-11-30'.format(year)
        charMonth = 'Nov'
    elif month == 'Dec' or month == 12:
        startDate = '{}-12-01'.format(year)
        endDate = '{}-12-31'.format(year)
        charMonth = 'Dec'

    return {
        'startDate': startDate,
        'endDate': endDate,
        'charMonth': charMonth
    }


# get percentage values and colour  of given two lists
def getFraction(list_x, list_y, purpose):
    size = len(list_x)
    list_z = [0] * size
    colour = [""] * size
    if purpose == 0:
        for index, (x, y, z) in enumerate(zip(list_x, list_y, list_z)):
            list_z[index] = int((x / y) * 100)

            if 0 <= list_z[index] <= 25:
                colour[index] = "success"
            elif 25 < list_z[index] <= 50:
                colour[index] = "primary"
            elif 50 < list_z[index] <= 75:
                colour[index] = "warning"
            elif 75 < list_z[index] <= 100:
                colour[index] = "danger"
            else:
                colour[index] = "danger"
                list_z[index] = 100
    if purpose == 1:
        for index, (x, y, z) in enumerate(zip(list_x, list_y, list_z)):
            list_z[index] = int((x / y) * 100)

            if 0 <= list_z[index] <= 25:
                colour[index] = "green"
            elif 25 < list_z[index] <= 50:
                colour[index] = ""
            elif 50 < list_z[index] <= 75:
                colour[index] = "yellow"
            elif 75 < list_z[index] <= 100:
                colour[index] = "red"
            else:
                colour[index] = "red"
                list_z[index] = 100

    return {'list_z': list_z,
            'colour': colour}
