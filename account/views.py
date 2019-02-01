from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.utils.http import is_safe_url


def registration_view(request):
    next = request.POST.get('next')
    next_post = request.GET.get('next')
    redirect_path = next or next_post or None
    form = UserRegistrationForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect('messapp:index')
    else:
        if form.is_valid():
            instance = form.save()
            return redirect("account:login")
            # login(user=instance.username, password=instance.password2)
            # if is_safe_url(redirect_path, request.get_host()):
            #     return redirect(redirect_path)
        else:
            print(form)

    return render(request, 'registration.html', {'form': form})


def login_view(request):
    next = request.POST.get('next')
    next_post = request.GET.get('next')
    rediect_path = next or next_post or None
    user = request.POST.get('username')
    password = request.POST.get('pass')
    auth = authenticate(request, username=user, password=password)
    if request.user.is_authenticated:
        print("loged user")
        return redirect('messapp:index')
    else:
        print("not Loged user")
        if auth is not None:
            login(request, auth)
            if is_safe_url(rediect_path, request.get_host()):
                return redirect(rediect_path)
            return redirect('messapp:index')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('account:login')