from django.contrib import admin
from .models import Costumer, UserChatMessage

admin.site.register([Costumer, UserChatMessage])
