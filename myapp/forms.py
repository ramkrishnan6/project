from django import forms
from django.contrib.auth.models import User
from myapp.models import Profile, Budget


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class GetBudgetForm(forms.ModelForm):
    automobile = forms.IntegerField()
    bank = forms.IntegerField()
    cash = forms.IntegerField()
    education = forms.IntegerField()
    entertainment = forms.IntegerField()
    fine = forms.IntegerField()
    food = forms.IntegerField()
    health = forms.IntegerField()
    other = forms.IntegerField()
    paytm = forms.IntegerField()
    recharge = forms.IntegerField()
    shopping = forms.IntegerField()
    travel = forms.IntegerField()
    upi = forms.IntegerField()

    class Meta:
        model = Budget
        fields = [
            'automobile',
            'bank',
            'cash',
            'education',
            'entertainment',
            'fine',
            'food',
            'health',
            'other',
            'paytm',
            'recharge',
            'shopping',
            'travel',
            'upi',
            'month']
