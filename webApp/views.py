from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.views import LoginView    
from django.shortcuts import render, redirect
from .forms import RegisterForm


def index(response):
    return render(response, "webApp/index.html", {})


def signin(response):
    if response.POST.get("signin_submit"):
        from django.contrib.auth import authenticate
        user = authenticate(username=response.POST.get('user-name'), password=response.POST.get('password'))
        if user is not None:
            pass
        else:
            messages.error(response, 'Failed to login. Please check username or password')
        

    return render(response, "webApp/signin.html", {})


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form":form})