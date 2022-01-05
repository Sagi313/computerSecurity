from django.contrib.auth import authenticate, login, logout
from django.http import response
from django.contrib import messages
from django.shortcuts import render, redirect
from webApp.core import is_input_text_valid, is_valid_name, is_valid_email
from .forms import RegisterForm, PasswordChangingForm
from webApp.models import Costumer, UserChatMessage, UserLoginTry
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
import json

with open("webApp/config/pass.json") as file:
    rules = json.load(file)


@login_required(login_url='/login/')
def index(response):
    if response.method == 'POST':
        if response.POST.get("submit"):
            if (not is_input_text_valid(response.POST.get('costumer_name'), 256, 1)) or (
            not is_valid_name(response.POST.get('costumer_name'))):
                messages.error(response, f'Costumer name is invalid')
                return redirect('/')
            elif (not is_input_text_valid(response.POST.get('costumer_email'), 256, 1)) or (
            not is_valid_email(response.POST.get('costumer_email'))):
                messages.error(response, f'Costumer email is invalid')
                return redirect('/')
            elif not is_input_text_valid(response.POST.get('costumer_info'), 256, 1):
                messages.error(response, f'Costumer info is invalid')
                return redirect('/')

            new_costumer = Costumer(sales_person=response.user, name=response.POST.get('costumer_name'),
                                    email=response.POST.get('costumer_email'), info=response.POST.get('costumer_info'))
            new_costumer.save()

            messages.success(response, f'Costumer {new_costumer.name} added successfully')

        if response.POST.get("delete_costumers"):
            for key in response.POST:
                if "delete-costumer_" in key:
                    to_delete_id = key.split("_")[1]
                    to_delete_costumer = Costumer.objects.get(id=int(to_delete_id))
                    costumer_name = to_delete_costumer.name
                    if to_delete_costumer.sales_person == response.user:
                        to_delete_costumer.delete()

                        messages.success(response, f'Costumer {costumer_name} was deleted')
                    else:
                        messages.error(response, f"Your trying to do an action that you shouldn't")
        ### VULENARABLE INPUT FIELD ###
        if response.POST.get('search-bar-submit'):
            return search_results(response)

        return redirect('/')

    all_costumers = Costumer.objects.all()

    return render(response, "webApp/index.html", {'costumers': all_costumers})


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            new_user = authenticate(username=username,
                                    password=form.cleaned_data['password1'], )
            user_login = UserLoginTry(user_name=username, counter_tries_login=0,
                                      time_last_try=timezone.now() + datetime.timedelta(hours=2))
            user_login.save()
            login(response, new_user)

            return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form": form})


def search_results(response):  # This view has the search bar who is vulnerable to SQL injection
    current_user = response.user
    query = response.POST.get('search-bar')
    results = []
    for result in list(Costumer.objects.filter(name=query, sales_person_id=current_user.id)):
        results.append(result.__dict__)

    return render(response, "webApp/search_results.html", {'results': results})


class changepasswordsform(PasswordChangeView):
    class_form = PasswordChangeForm


@login_required(login_url='/login/')
def password_success(request):
    return render(request, "registration/password_success.html")


@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/login')


def chat(response):
    if response.method == "POST":
        if not is_input_text_valid(response.POST.get('user_message'), 100, 1):
            messages.error(response, f'Message is invalid')
        user_chat_msg = UserChatMessage(user_name=response.user, message_box=response.POST.get("user_message"))
        user_chat_msg.save()

        return redirect("/chat")

    msg = UserChatMessage.objects.all()
    return render(response, "webApp/chat.html", {'chat_msgs': msg})


def about(request):
    return render(request, "webApp/about.html")


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username in [user.username for user in User.objects.all()]:
            user_check = UserLoginTry.objects.get(user_name=username)
            lock_down_seconds = rules["lock_down_time"]
            time_to_lock = user_check.time_last_try + datetime.timedelta(seconds=lock_down_seconds)
            if (timezone.now() + datetime.timedelta(hours=2) - user_check.time_last_try) < datetime.timedelta(
                    seconds=lock_down_seconds) and user_check.counter_tries_login > rules["Max_retries"]:
                messages.error(request, "Please wait until {:%d, %b %Y, %H:%M:%S}".format(time_to_lock))
                return redirect('/')
            user = authenticate(request, username=username, password=password)
            if user:
                if user_check.counter_tries_login < rules["Max_retries"]:
                    user_check.counter_tries_login = 0
                    user_check.save()
                    login(request, user)
                    return redirect('/')
            else:
                user = UserLoginTry.objects.get(user_name=username)
                user.counter_tries_login = user.counter_tries_login + 1
                user.time_last_try = timezone.now() + datetime.timedelta(hours=2)
                user.save()
                messages.error(request, f'Incorrect password for user {username}')
        else:
            messages.error(request, f'User {username} does not exist')

        return redirect("/login")

    return render(request, 'registration/login.html')
