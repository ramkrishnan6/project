from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField('Date of Transaction')
    description = models.CharField(max_length=50)
    cost = models.IntegerField(default=0)
    category = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.description
