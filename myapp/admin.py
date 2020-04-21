from django.contrib import admin
from .models import User
from .models import ManualInputDB
# Register your models here.


admin.site.register(User)
admin.site.register(ManualInputDB)
