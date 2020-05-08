from django.contrib import admin
from .models import Transaction
from .models import Budget

admin.site.register(Transaction)
admin.site.register(Budget)
