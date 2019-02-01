from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db.models import Sum
from django.db.models.signals import pre_save

today_date = timezone.datetime.now().date()
next_day = today_date + timedelta(1)


class MemberQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(active=True)

    def expense(self, pk):
        return self.filter(pk=pk).expense_set.all()

    def deposits(self):
        total_deposit = Deposit.objects.filter(member=self.pk)
        return total_deposit


class MemberManager(models.Manager):

    def get_queryset(self):
        return MemberQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def member_expense(self, pk):
        return self.get_queryset().expense(pk)

    def total_depo(self):
        return self.get_queryset().deposits()


class Member(models.Model):
    name = models.CharField(max_length=50)
    phone = models.PositiveIntegerField(blank=True, null=True)
    timestimp = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = MemberManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('messapp:member_details', kwargs={'pk': self.pk})

    @property
    def total_deposit(self):
        return self.total_depo()


class Deposit(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    timestimp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member.username

    # @property
    # def member_deposit(self):
    #     total_deposit = Deposit.objects.filter(member=self.member).aggregate(Sum("total"))["total_sum"]
    #     return total_deposit

MEAL_TIME = (
    ('breakfast', 'Breakfast'),
    ('launch', 'Launch'),
    ('dinner', 'Dinner')
)



class ExpenseQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(active=True)

    def breakfast(self):
        # day = datetime.
        return self.filter(meal_type='breakfast', date=today_date)

    def launch(self):
        return self.filter(meal_type='launch', date=today_date)

    def dinner(self):
        return self.filter(meal_type='dinner', date=today_date)


class ExpenseManager(models.Manager):

    def get_queryset(self):
        return ExpenseQuerySet(self.model, using=self._db)

    def breakfast(self):
        return self.get_queryset().breakfast().active()

    def launch(self):
        return self.get_queryset().launch().active()

    def dinner(self):
        return self.get_queryset().dinner().active()


class Expense(models.Model):
    meal_type = models.CharField(max_length=20, choices=MEAL_TIME, blank=True, null=True, verbose_name="Expense Type")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name="Item Name")
    price = models.DecimalField(decimal_places=2, max_digits=8)
    details = models.TextField(blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    timestimp = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = ExpenseManager()

    def __str__(self):
        return self.name


class Meal(models.Model):
    member = models.ForeignKey(User, models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TIME, blank=True, null=True)
    total = models.PositiveIntegerField()
    date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)

    def __str__(self):
        return self.member.username

    class Meta:
        verbose_name_plural = 'Meal'
        verbose_name = 'Meal By'

# def meal_total_Pre_save(sender, instance, *args, **kwargs):
#s
#
# pre_save.connect(meal_total_Pre_save, sender=Meal)

