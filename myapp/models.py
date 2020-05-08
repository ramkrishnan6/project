from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField('Date of Transaction')
    description = models.CharField(max_length=100)
    cost = models.IntegerField(default=0)

    categories = [
        ('Automobile', 'Automobile'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash Withdrawal', 'Cash Withdrawal'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Fine', 'Fine'),
        ('Food', 'Food'),
        ('Health Care', 'Health Care'),
        ('Other', 'Other'),
        ('Paytm', 'Paytm'),
        ('Recharge', 'Recharge'),
        ('Shopping', 'Shopping'),
        ('Travel', 'Travel'),
        ('UPI', 'UPI')
    ]

    category = models.CharField(
        max_length=30,
        choices=categories
    )

    def __str__(self):
        return "{} - {} - {}".format(self.user_id, self.category, self.cost)


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    automobile = models.IntegerField(default=0)
    bank = models.IntegerField(default=0)
    cash = models.IntegerField(default=0)
    education = models.IntegerField(default=0)
    entertainment = models.IntegerField(default=0)
    fine = models.IntegerField(default=0)
    food = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    other = models.IntegerField(default=0)
    paytm = models.IntegerField(default=0)
    recharge = models.IntegerField(default=0)
    shopping = models.IntegerField(default=0)
    travel = models.IntegerField(default=0)
    upi = models.IntegerField(default=0)

    months = [
        ('Jan', 'Jan'),
        ('Feb', 'Feb'),
        ('Mar', 'Mar'),
        ('Apr', 'Apr'),
        ('May', 'May'),
        ('Jun', 'Jun'),
        ('Jul', 'Jul'),
        ('Aug', 'Aug'),
        ('Sep', 'Sep'),
        ('Oct', 'Oct'),
        ('Nov', 'Nov'),
        ('Dec', 'Dec'),
        ('None', 'None'),
    ]
    month = models.CharField(
        max_length=30,
        choices=months,
        default='None',
    )
    def __str__(self):
        return "{} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {}".format(
            self.user, self.automobile, self.bank, self.cash,
             self.education, self.entertainment, self.fine,
             self.food, self.health, self.other, self.paytm,
             self.recharge, self.shopping, self.travel, self.upi,
             self.month
        )
