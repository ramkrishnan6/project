from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField('Date of Transaction')
    description = models.CharField(max_length=50)
    cost = models.IntegerField(default=0)
    #category = models.CharField(max_length=20, blank=True, null=True)


    categoryArray = [
        ('Automobile', 'Automobile'),
        ('Bank_Transfer', 'Bank Transfer'),
        ('Cash_Withdrawal', 'Cash Withdrawal'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Fine', 'Fine'),
        ('Food', 'Food'),
        ('Health_Care', 'Health Care'),
        ('Paytm', 'PayTM'),
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
        return self.description
