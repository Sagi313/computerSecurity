from django.contrib.auth import authenticate, login, logout
from django.http import response
from django.contrib import messages
from django.shortcuts import render, redirect
from webApp.core import is_input_text_valid
from .forms import RegisterForm, PasswordChangingForm
from webApp.models import Costumer, UserChatMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


@login_required(login_url='/login/')
def index(response):
    if response.method == 'POST':
        if response.POST.get("submit"):
            if not is_input_text_valid(response.POST.get('costumer_name'), 256, 1):
                messages.error(response, f'Costumer name is invalid')
                return redirect('/')
            elif not is_input_text_valid(response.POST.get('costumer_email'), 256, 1):
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
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'], )
            login(response, new_user)

            return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form": form})


def search_results(response):  # This view has the search bar who is vulnerable to SQL injection
    current_user = response.user
    query = response.POST.get('search-bar')
    if query:
        # To exploit this input field, enter "%' -- " in the search bar (without the quotes)
        sql = f"SELECT * FROM webapp_costumer WHERE name LIKE '%{query}%' AND sales_person_id = {current_user.id};"

    try:
        import mysql.connector

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="computersecurity"
        )
        cursor = mydb.cursor()
        results = []

        iterable = cursor.execute(sql, multi=True)  # Allows multi query, this way we can use UNION in our SQL Injection
        for result in iterable:
            results += (result.fetchall())

    except Exception as e:
        print(e)
        results = []

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
        if not is_input_text_valid(response.POST.get('user_message'), 256, 1):
            messages.error(response, f'Message is invalid')
        user_chat_msg = UserChatMessage(user_name=response.user, message_box=response.POST.get("user_message"))
        user_chat_msg.save()
    msg = UserChatMessage.objects.all()
    return render(response, "webApp/chat.html", {'chat_msgs': msg})

def about(request):
    return render(request, "webApp/about.html")

def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username in [user.username for user in User.objects.all()]:
            user=authenticate(request ,username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                messages.error()
    else:
        print("hey")
    context = {}
    return render(request,'registration/login.html', context)
