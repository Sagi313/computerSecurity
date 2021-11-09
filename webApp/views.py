from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.

def index(response):
    return HttpResponse("Hello, world.")

def register(response):
    if response.POST.get("register_submit"):
        try:
            if response.POST.get('password') == response.POST.get('password-confirm'):
                from django.contrib.auth.models import User
                user = User.objects.create_user(username=response.POST.get('user-name'),email=response.POST.get('email'),password=response.POST.get('password'))

                full_name = response.POST.get('full-name').split()
                user.last_name, user.first_name = full_name[1], full_name[0]
                user.save()

                messages.success(response, f'full_name, your account has been created successfully')
            else:
                messages.error(response, 'Password does not match')
        except:
            messages.error(response, 'Failed to create account')
            pass
    
    return render(response, "webApp/register.html", {})
