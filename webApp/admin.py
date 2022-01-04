from django.contrib import admin
from .models import Costumer, UserChatMessage, UserLoginTry

admin.site.register([Costumer, UserChatMessage, UserLoginTry])
