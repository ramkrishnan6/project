from django.contrib import admin
from .models import Transaction
from .models import Budget
from .models import Profile

admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Profile)
