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
    automobile = models.IntegerField(default=1000)
    bank = models.IntegerField(default=1000)
    cash = models.IntegerField(default=1000)
    education = models.IntegerField(default=1000)
    entertainment = models.IntegerField(default=1000)
    fine = models.IntegerField(default=1000)
    food = models.IntegerField(default=1000)
    health = models.IntegerField(default=1000)
    other = models.IntegerField(default=1000)
    paytm = models.IntegerField(default=1000)
    recharge = models.IntegerField(default=1000)
    shopping = models.IntegerField(default=1000)
    travel = models.IntegerField(default=1000)
    upi = models.IntegerField(default=1000)

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
    ]
    month = models.CharField(
        max_length=30,
        choices=months,
        default='None',
    )

    def __str__(self):
        return "{} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {}".format(
            self.user, self.automobile, self.bank, self.cash, self.education, self.entertainment,
            self.fine, self.food, self.health, self.other, self.paytm, self.recharge, self.shopping,
            self.travel, self.upi, self.month)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

