from django.contrib.auth import authenticate, login , logout
from django.http import response
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from webApp.core import is_input_text_valid
from .forms import RegisterForm , PasswordChangingForm
from webApp.models import Costumer
from django.contrib.auth.decorators import login_required


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

            messages.success(response, f'Costumer {new_costumer.name} added succuessfully')

        if response.POST.get("delete_costumers"):
            for key in response.POST:
                if "delete-costumer_" in key:
                    to_delete_id = key.split("_")[1]
                    to_delete_costumer = Costumer.objects.get(id=int(to_delete_id))
                    costumer_name = to_delete_costumer.name
                    to_delete_costumer.delete()

                    messages.success(response, f'Costumer {costumer_name} was deleted')

        return redirect('/')

    all_costumers = Costumer.objects.all()
    relevant_costumers = [costumer for costumer in all_costumers if costumer.sales_person == response.user]

    return render(response, "webApp/index.html", {'costumers': relevant_costumers})


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        #print(f"respone {response.POST}", flush=True)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'], )
            login(response, new_user)

            return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form": form})

  
def password_change(response):
    if response.method == "POST":
        try:
            form = PasswordChangingForm(response.POST)
            print(f"respone {response.POST}",flush=True)
            print(response.user, flush=True)
            new_user = authenticate(username=response.user,password=response.POST.get('new_password'),)
            login(response, new_user)
            messages.success(response, f'Password changed succuessfuly. Please go back to main page')
        except:
            messages.error(response, f'Failed to change password')

    else:
        form = PasswordChangingForm(response.POST)

    return render(response, "registration/change-password.html", {"form":form})


def logout_user(request):
	logout(request)
	return redirect('login')

