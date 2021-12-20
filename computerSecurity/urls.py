from django.contrib import admin
from django.urls import path,include
from django.urls.conf import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('webApp.urls')),
    path('admin/', admin.site.urls), 
]
