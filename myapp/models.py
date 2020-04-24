from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField('Date of Transaction')
    description = models.CharField(max_length=50)
    cost = models.IntegerField(default=0)


    categoryArray = [
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
        ('Unknown', 'Unknown'),
        ('UPI', 'UPI')

    ]
    category = models.CharField(
        max_length=30,
        choices=categoryArray,
        default='Unknown',
    )

    def is_upperclass(self):
        return self.category

    def __str__(self):
        return "{} - {} - {}".format(self.user_id, self.category, self.cost)
