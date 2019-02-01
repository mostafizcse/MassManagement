from django import forms
from .models import *


class MemberForm(forms.ModelForm):
    class Meta:
        models = Member
        fields = '__all__'


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = '__all__'


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = '__all__'
        exclude = ('member',)


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
