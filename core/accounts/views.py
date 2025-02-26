
from django.shortcuts import render, redirect
from django.urls import  reverse
from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegisterForm, CustomLoginForm
from accounts.models import CustomUser
from django.contrib import messages

# ثبت‌نام کاربر
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "ثبت‌نام با موفقیت انجام شد! حالا وارد شوید.")
            return redirect(reverse('accounts:login'))
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


# ورود کاربر
def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('blog:index'))

    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "ورود موفقیت‌آمیز بود!")
            return redirect(reverse('blog:index'))
    else:
        form = CustomLoginForm()
    return render(request, "registration/login.html", {"form": form})


# خروج کاربر
def logout_view(request):
    logout(request)
    messages.success(request, "شما با موفقیت خارج شدید!")
    return redirect(reverse('blog:index'))
