import statistics

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
    category_wise_expenditure = [0] * 14

    for index, x in enumerate(categories):
        transaction_all = Transaction.objects.filter(user_id=request.user.id, category=x,
                                                     date__range=[startDate, endDate])
        for transaction in transaction_all:
            category_wise_expenditure[index] = category_wise_expenditure[index] + transaction.cost

    total = sum(category_wise_expenditure)

    return {
        'category_wise_expenditure': category_wise_expenditure,
        'total': total,
    }


# get budget value and total of the values of a particular month
def showBudget(request, month):
    budgetValues = Budget.objects.filter(user_id=request.user.id, month=month)
    category_wise_budget = [0] * 14

    for index, x in enumerate(budgetValues):
        category_wise_budget = [x.automobile, x.bank, x.cash, x.education, x.entertainment, x.fine, x.food,
                                x.health, x.other, x.paytm, x.recharge, x.shopping, x.travel, x.upi]
    budgetTotal = (
            x.automobile + x.bank + x.cash + x.education + x.entertainment + x.fine + x.food + x.health + x.other + x.paytm + x.recharge + x.shopping + x.travel + x.upi)
    budgetTotal = int(budgetTotal)

    return {'category_wise_budget': category_wise_budget, 'budgetTotal': budgetTotal}


# get MONTH-WISE total of each category of TRANSACTIONS, corresponding BUDGET VALUE, COLOUR (in terms of bootstrap),
# and percentage of a given year
def calculateMonthlyTotal(request, year):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_expenditure = [0] * 12
    monthly_budget = [0] * 12

    for index, x in enumerate(months):
        buffer = getDate(x, year)
        startDate = buffer['startDate']
        endDate = buffer['endDate']
        monthly_budget[index] = showBudget(request, x)["budgetTotal"]

        transaction_all = Transaction.objects.filter(user_id=request.user.id, date__range=[startDate, endDate])
        for transaction in transaction_all:
            monthly_expenditure[index] = monthly_expenditure[index] + transaction.cost

    buffer = getFraction(monthly_expenditure, monthly_budget, 1)
    progress_colour = buffer['progress_colour']
    monthly_total_percentage = buffer['list_z']

    return {'monthly_expenditure': monthly_expenditure, 'progress_colour': progress_colour, 'monthly_budget': monthly_budget,
            'monthly_total_percentage': monthly_total_percentage}


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


# get percentage values and colour of given two lists
def getFraction(list_x, list_y, purpose):
    size = len(list_x)
    list_z = [0] * size
    progress_colour = [""] * size
    if purpose == 0:
        for index, (x, y, z) in enumerate(zip(list_x, list_y, list_z)):
            list_z[index] = int((x / y) * 100)
            if 0 <= list_z[index] <= 25:
                progress_colour[index] = "success"
            elif 25 < list_z[index] <= 50:
                progress_colour[index] = "primary"
            elif 50 < list_z[index] <= 75:
                progress_colour[index] = "warning"
            elif 75 < list_z[index] <= 100:
                progress_colour[index] = "danger"
            else:
                progress_colour[index] = "danger"
                list_z[index] = 100
    if purpose == 1:
        for index, (x, y, z) in enumerate(zip(list_x, list_y, list_z)):
            list_z[index] = int((x / y) * 100)

            if 0 <= list_z[index] <= 25:
                progress_colour[index] = "green"
            elif 25 < list_z[index] <= 50:
                progress_colour[index] = ""
            elif 50 < list_z[index] <= 75:
                progress_colour[index] = "yellow"
            elif 75 < list_z[index] <= 100:
                progress_colour[index] = "red"
            else:
                progress_colour[index] = "red"
                list_z[index] = 100

    return {'list_z': list_z,
            'progress_colour': progress_colour}


# get the maximum value of the list amd its corresponding field
def getMax(listX, listY, fields):
    print("in d.py/ getMax")
    maxValue = max(listX)
    maxValueIndex = listX.index(maxValue)
    categories = fields

    most_expensive_category = categories[maxValueIndex]
    correspondingBudget = listY[maxValueIndex]
    maxInfo = {
        'maxValue': maxValue,
        'most_expensive_category': most_expensive_category,
        'correspondingBudget': correspondingBudget,
        'maxValueIndex': maxValueIndex,
    }
    print(most_expensive_category)
    print("d.py/getMax endfunc")
    return maxInfo


# get the summary of a list
def summarize(listX, listY, year, purpose):
    print("in d.py/ summarize")
    # purpose 0 - for the whole year
    # purpose 1 - for the categories of that range
    # monthlyTotal is     [4777,  5243,   8221,   11971,  12711,  7721,   1400,   0,      0,      0,      0,      0]
    # monthlyBudget is  [9100,  14000,  16000,  12351,  14000,  15850,  14000,  19800,  14000,  14000,  14000,  14000]
    # percentage is       [52,    37,     51,     96,     60,     48,     10,     0,      0,      0,      0,      0]

    # categoryTotal is [700, 178, 3000, 1540, 500, 500, 1258, 150, 37, 100, 547, 1390, 2712, 99]
    # budgetList is [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]

    summaryMonthly = ""
    summaryCategory = ""
    overBudgetCount = 0
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    categories = ["Automobile", "Bank Transfer", "Cash Withdrawal", "Education", "Entertainment", "Fine",
                  "Food", "Health Care", "Other", "Paytm", "Recharge", "Shopping", "Travel", "UPI"]
    length = len(listX)
    key_value = {}
    # field = []

    if purpose == 0:
        field = months
        for i in range(0, length):
            key_value[months[i]] = listX[i]
        key_value = sorted(key_value.items(), key=lambda kv: (kv[1], kv[0]))
        percentage = getFraction(listX, listY, 0)["list_z"]
        buffer = summarizePercentages(percentage)
        percentage_75 = buffer["percentage_75"]
        percentage_90 = buffer["percentage_90"]
        percentage_100 = buffer["percentage_100"]
        buffer = getMax(listX, listY, field)
        maxValue = buffer["maxValue"]
        most_expensive_category = buffer["most_expensive_category"]
        correspondingBudget = buffer["correspondingBudget"]
        maxValueIndex = buffer["maxValueIndex"]
        most_expensive_month = months[maxValueIndex]
        for i, j in zip(listX, listY):
            if i > j:
                overBudgetCount += 1
        mean = int((sum(listX)) / length)
        median = statistics.median(listX)
        print(median)
        print(percentage_75)                # [0, 1, 2, 5, 6]
        print(percentage_90)                # [3, 4]
        print(percentage_100)               # []
        print(percentage)
        if len(percentage_75) != 0:
            summaryMonthly = summaryMonthly + "Months where you have spent reasonably: "                    # < 75
            for value in percentage_75:
                summaryMonthly = summaryMonthly + "{} ".format(months[value])
            summaryMonthly = summaryMonthly + ". "

        if len(percentage_90) != 0:
            summaryMonthly = summaryMonthly + "Months where you could have saved a bit more money: "
            for value in percentage_90:
                summaryMonthly = summaryMonthly + "{} ".format(months[value])
            summaryMonthly = summaryMonthly + ". "

        if len(percentage_100) != 0:
            summaryMonthly = summaryMonthly + "YOU HAVE GONE OVER BUDGET IN THE MONTH/S OF "
            for value in percentage_90:
                summaryMonthly = summaryMonthly + "{} ".format(months[value])
            summaryMonthly = summaryMonthly + ". "

        summaryMonthly = summaryMonthly + "On an average you spend ₹{} monthly.".format(mean)
        summaryMonthly = summaryMonthly + "You have spent maximum in the month of {}, which is {} for which your budget was {}.".format(most_expensive_month, maxValue, correspondingBudget)

# elif purpose == 1:
#     field = categories
#     for i in range(0, length):
#         key_value[categories[i]] = listX[i]
#     key_value = sorted(key_value.items(), key=lambda kv: (kv[1], kv[0]))
#     percentage = getFraction(listX, listY, 0)["list_z"]
#     buffer = getMax(listX, listY, field)
#     maxValue = buffer["maxValue"]
#     most_expensive_category = buffer["most_expensive_category"]
#     correspondingBudget = buffer["correspondingBudget"]
#     for i, j in zip(listX, listY):
#         if i > j:
#             overBudgetCount += 1
#     mean = int((sum(listX)) / length)
#     print("key value is", key_value)
#     print("percentage is", percentage)
#     print("overBudgetCount is", overBudgetCount)
#     print("mean is", mean)
#     print("maxvalue is ", maxValue)
#     print("maxcategory is ", most_expensive_category)
#     print("correspondingBudget is ", correspondingBudget)
#     summaryCategory = summaryCategory + "On an average you have spent {} monthly. ".format(mean)
#     summaryCategory = summaryCategory + " percentage is {} ".format(percentage)
#     summaryCategory = summaryCategory + " overBudgetCount is {} ".format(overBudgetCount)
#     summaryCategory = summaryCategory + " mean is {} ".format(mean)
#     summaryCategory = summaryCategory + " maxvalue is {} ".format(maxValue)
#     summaryCategory = summaryCategory + " correspondingBudget is {} ".format(correspondingBudget)
    summary = [summaryMonthly, summaryCategory]
    print("d.py/summarize endfunc")
    return summary


def summarizePercentages(percentage):

    percentage_75 = []      # < 75
    percentage_90 = []      # 75 - 100
    percentage_100 = []     # 100 >

    for value in percentage:
        if value == 0:
            break
        elif value < 75 or value == 75:
            percentage_75.append(percentage.index(value))
        elif 75 < value < 100:
            percentage_90.append(percentage.index(value))
        elif value == 100:
            percentage_100.append(percentage.index(value))

    percentage_dict = {
        'percentage_75': percentage_75,
        'percentage_90': percentage_90,
        'percentage_100': percentage_100,
    }
    return percentage_dict
