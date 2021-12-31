from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.http import request, response
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from webApp.core import is_input_text_valid
from .forms import RegisterForm , PasswordChangingForm 
from webApp.models import Costumer, UserChatMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser 

@login_required(login_url='/login/')
def index(response):
    if response.method == 'POST':
        if response.POST.get("submit"):
            if not is_input_text_valid(response.POST.get('costumer_name'), 256):
                messages.success(response, f'Costumer name is invalid')
                return redirect('/')
            elif not is_input_text_valid(response.POST.get('costumer_email'), 256):
                messages.success(response, f'Costumer email is invalid')
                return redirect('/')
            elif not is_input_text_valid(response.POST.get('costumer_info'), 256):
                messages.success(response, f'Costumer info is invalid')
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
                    to_delete_costumer.delete()

                    messages.success(response, f'Costumer {costumer_name} was deleted')

        ### VULENARABLE INPUT FIELD ###
        if response.POST.get('search-bar-submit'):
            return search_results(response)

        return redirect('/')

    all_costumers = Costumer.objects.all()
    relevant_costumers = [costumer for costumer in all_costumers if costumer.sales_person == response.user]

    return render(response, "webApp/index.html", {'costumers': relevant_costumers})

 
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


@login_required(login_url='/login/')
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
        cursor.execute(sql)

        results = cursor.fetchall()

    except:
        results = []

    return render(response, "webApp/search_results.html", {'results': results})


def password_change(response):
    if response.method == "POST":
        try:
            form = PasswordChangingForm(response.POST)
            print(f"respone {response.POST}", flush=True)
            print(response.user, flush=True)
            new_user = authenticate(username=response.user, password=response.POST.get('new_password'), )
            login(response, new_user)
            messages.success(response, f'Password changed succuessfuly. Please go back to main page')
        except:
            messages.error(response, f'Failed to change password')


    else:
        form = PasswordChangingForm(response.POST)

    return render(response, "registration/change-password.html", {"form": form})


def logout_user(request):
	logout(request)
	return redirect('login')

def chat(response):
    if response.method == "POST":
        user_chat_msg=UserChatMessage(user_name=response.user , message_box=response.POST.get("user_message"))
        user_chat_msg.save()
    msg = UserChatMessage.objects.all()
    return render(response, "webApp/chat.html", {'chat_msgs':msg})





