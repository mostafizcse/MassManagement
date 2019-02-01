from django.urls import path
from . import views

app_name = 'messApp'

urlpatterns = [
    path('', views.index, name="index"),
    # path('member/', views.MemberView.as_view(), name='member'),
    # path('member/<pk>', views.MemberDetails.as_view(), name="member_details"),
    path('dashbroad/<username>', views.member_dashbroad, name="dash_broad"),
    path('expense/', views.ExpenseView.as_view(), name="expense"),
    path('deposit/', views.balance_view, name="balance"),
    path('breakfast/', views.breakfastview, name="breakfast"),
    path('launch/', views.launchview, name="launch"),
    path('dinner/', views.dinnerview, name="dinner"),
    path('meal/', views.mealview, name="meal"),
]