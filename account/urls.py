from django.urls import path
from .views import *

app_name = 'account'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('registration/', registration_view, name='registration'),
    path('logout/', logout_view, name='logout')
]