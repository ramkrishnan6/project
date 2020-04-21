from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)


class ManualInputDB(models.Model):
    description = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    cost = models.AutoField
    doft = models.DateField()

