from django.contrib import admin
from .models import Member, Deposit, Expense, Meal


class MemberAdmin(admin.ModelAdmin):

    list_display = ['name', 'phone', 'active', 'timestimp']

    class Meta:
        model = Member


admin.site.register(Member, MemberAdmin)


class DepositAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'total', 'timestimp']

    class Meta:
        model = Deposit


admin.site.register(Deposit, DepositAdmin)


class ExpenseAdmin(admin.ModelAdmin):

    list_display = ['name', 'buyer', 'price', 'meal_type', 'active', 'date']
    list_filter = ['meal_type', 'timestimp']

    class Meta:
        model = Expense


admin.site.register(Expense, ExpenseAdmin)


class MealAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'meal_type', 'date', 'total']
    list_filter = ['member', 'meal_type', 'date']

    class Meta:
        model = Meal


admin.site.register(Meal, MealAdmin)
