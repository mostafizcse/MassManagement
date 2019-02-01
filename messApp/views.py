import math
from django.shortcuts import render, redirect
from django.views import generic
from .models import Member, Expense, Meal, Deposit
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from django.views.generic.edit import FormMixin
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import DepositForm, MealForm, ExpenseForm

today_date = timezone.datetime.now().date()
next_day = today_date + timedelta(1)
next_two_day = today_date + timedelta(2)
next_third_day = today_date + timedelta(3)
next_four_day = today_date + timedelta(4)
next_five_day = today_date + timedelta(5)
next_six_day = today_date + timedelta(6)
current_month = timezone.datetime.now().date().month
current_year = timezone.datetime.now().date().year





def index(request):
    return render(request, 'index.html')


class MemberView(generic.ListView):
    model = Member
    template_name = 'messapp/member.html'


class MemberDetails(generic.DetailView):
    model = Member
    template_name = 'messapp/member_details.html'
    context_object_name = 'member_details'

    def get_context_data(self, *args, **kwargs):
        context = super(MemberDetails, self).get_context_data(*args, **kwargs)
        pk = self.kwargs.get('pk')
        self_obj = Member.objects.filter(pk=pk)
        total_expense_obj = Member.objects.get(pk=pk).expense_set.all().aggregate(Sum('price'))['price__sum']
        total_expense = Expense.objects.filter(date__month=current_month, date__year=current_year).aggregate(Sum('price'))['price__sum']
        total_meal = Meal.objects.filter(date__month=current_month, date__year=current_year).aggregate(Sum('total'))['total__sum']


        self_total_meal = Member.objects.get(pk=pk).meal_set.filter(date__month=current_month, date__year=current_year).aggregate(Sum('total'))['total__sum']
        self_total_deposit = Member.objects.get(pk=pk).deposit_set.filter(date__month=current_month, date__year=current_year).aggregate(Sum('total'))['total__sum']

        if total_expense and total_meal is not None:
            rate_per_meal = total_expense / total_meal
        else:
            rate_per_meal = 0

        if self_total_meal and rate_per_meal is not None:
            self_meal_cost = self_total_meal * rate_per_meal
        else:
            self_meal_cost = "Nothing"

        if self_total_deposit and self_meal_cost is not None:
            total_balance = self_total_deposit - self_meal_cost
        else:
            total_balance = "Not Completed"
        context["self_total_meal"] = self_total_meal
        context['self_total_deposit'] = self_total_deposit
        context['total_expense'] = total_expense
        context["rate_per_meal"] = rate_per_meal
        context["self_meal_cost"] = self_meal_cost
        context["total_balance"] = total_balance

        return context


@login_required(login_url='account:login')
def member_dashbroad(request, username):
    template_name ='messapp/dashbroad.html'

    self_total_meal = Meal.objects.filter(date__month=current_month, date__year=current_year, member__username=username).aggregate(Sum('total'))['total__sum']
    total_expense = Expense.objects.filter(date__month=current_month, date__year=current_year).aggregate(Sum('price'))['price__sum']
    total_meal = Meal.objects.filter(date__month=current_month, date__year=current_year).aggregate(Sum('total'))['total__sum']
    print(request.user.username)

    self_expense_obj = Expense.objects.filter(date__month=current_month, date__year=current_year, buyer_id__username=username)
    self_expense_total = Expense.objects.filter(date__month=current_month, date__year=current_year, buyer_id__username=username).aggregate(Sum('price'))['price__sum']

    self_deposit_obj = Deposit.objects.filter(date__month=current_month, date__year=current_year,
                                              member__username=username)
    self_deposit_total = Deposit.objects.filter(date__month=current_month, date__year=current_year,
                                              member__username=username).aggregate(Sum('total'))['total__sum']

    self_meal_obj = Meal.objects.filter(date__month=current_month, date__year=current_year,
                                              member__username=username)
    self_meal_total = Meal.objects.filter(date__month=current_month, date__year=current_year,
                                              member__username=username).aggregate(Sum('total'))['total__sum']
    if total_expense and total_meal is not None:
        rate_per_meal = total_expense / total_meal
    else:
        rate_per_meal = 0

    if self_total_meal and rate_per_meal is not None:
        self_meal_cost = self_total_meal * rate_per_meal
    else:
        self_meal_cost = "Nothing"

    context = {
        "self_total_meal": self_total_meal,
        "self_meal_cost": self_meal_cost,
        "rate_per_meal": rate_per_meal,

        "self_expense_obj": self_expense_obj,
        'self_expense_total': self_expense_total,
        "self_deposit_obj": self_deposit_obj,
        "self_deposit_total": self_deposit_total,
        "self_meal_obj": self_meal_obj,
        "self_meal_total": self_meal_total
    }
    return render(request, template_name, context)


@login_required(login_url='account:login')
def mealview(request):
    template_name = 'messapp/meal_list.html'
    # obj = Meal.objects.filter(date=today_date)
    obj = Meal.objects.filter(date__month=current_month, date__year=current_year, member=request.user)
    total_expense = Expense.objects.filter(date__month=current_month, date__year=current_year).aggregate(Sum('price'))['price__sum']
    total_meal = Meal.objects.filter(date__month=current_month, date__year=current_year).aggregate(Sum('total'))['total__sum']
    if total_expense and total_meal is not None:
        rate_per_meal = total_expense / total_meal
    else:
        rate_per_meal = "No meal in this month"

    form = MealForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.member = request.user
        instance.save()
        return redirect("messapp:meal")
    print(request.user.username)
    context = {
        'meal_list': obj,
        'total_expense': total_expense,
        'total_meal': total_meal,
         'rate_per_meal': rate_per_meal,
        'form': form,
        'current_month': current_month,
        'current_year': current_year
    }
    return render(request, template_name, context)


class ExpenseView(generic.ListView):
    model = Expense
    queryset = Expense.objects.filter(date__month=current_month, date__year=current_year)
    template_name = 'messapp/expense_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ExpenseView, self).get_context_data(*args, **kwargs)
        total = 0
        for cost in Expense.objects.filter(date__month=current_month, date__year=current_year):
            total += cost.price
            context['total_expense'] = total
        # context['form'] = self.get_form()
        return context


@login_required(login_url='account:login')
def balance_view(request):
    template_name = 'messapp/balance.html'

    deposit = Deposit.objects.all().aggregate(Sum('total'))['total__sum']
    members = Member.objects.all()
    # memeber_deposit = Member.objects.filter()
    obj = Deposit.objects.all()
    form = DepositForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('messapp:balance')

    context = {
        'obj': obj,
        'member_obj': members,
        'deposit': deposit,
        'form': form
    }

    return render(request, template_name, context)


@login_required(login_url='account:login')
def breakfastview(request):
    template_name = 'messapp/bazar.html'
    meal_type = 'breakfast'

    obj = Expense.objects.filter(date__month=current_month, date__year=current_year, meal_type="breakfast")
    next_day = today_date + timedelta(1)
    next_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_day)
    two_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_two_day)
    third_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_third_day)
    four_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_four_day)
    five_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_five_day)
    six_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_six_day)

    context = {
        'bazar_for': meal_type,
        'bazar_obj': obj,
        'tomorrow_obj': next_day_obj,
        'next_day': next_day,
        'two_day': two_day_obj,
        'third_day': third_day_obj,
        'four_day': four_day_obj,
        'five_day': five_day_obj,
        'six_day': six_day_obj,
    }
    return render(request, template_name, context)

@login_required(login_url='account:login')
def launchview(request):
    template_name = 'messapp/bazar.html'
    meal_type = 'launch'
    obj = Expense.objects.filter(date__month=current_month, date__year=current_year, meal_type="launch")
    next_day = today_date + timedelta(1)
    next_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_day)
    two_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_two_day)
    third_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_third_day)
    four_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_four_day)
    five_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_five_day)
    six_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_six_day)

    context = {
        'bazar_for': meal_type,
        'bazar_obj': obj,
        'tomorrow_obj': next_day_obj,
        'next_day': next_day,
        'two_day': two_day_obj,
        'third_day': third_day_obj,
        'four_day': four_day_obj,
        'five_day': five_day_obj,
        'six_day': six_day_obj,
    }
    return render(request, template_name, context)


@login_required(login_url='account:login')
def dinnerview(request):
    template_name = 'messapp/bazar.html'
    meal_type = 'dinner'
    obj = Expense.objects.filter(date__month=current_month, date__year=current_year, meal_type="dinner")
    next_day = today_date + timedelta(1)
    next_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_day)
    two_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_two_day)
    third_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_third_day)
    four_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_four_day)
    five_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_five_day)
    six_day_obj = Expense.objects.filter(meal_type=meal_type, date=next_six_day)
    context = {
        'bazar_for': meal_type,
        'bazar_obj': obj,
        'tomorrow_obj': next_day_obj,
        'next_day': next_day,
        'two_day': two_day_obj,
        'third_day': third_day_obj,
        'four_day': four_day_obj,
        'five_day': five_day_obj,
        'six_day': six_day_obj,
    }
    return render(request, template_name, context)
