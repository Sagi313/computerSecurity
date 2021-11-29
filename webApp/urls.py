from django.conf.urls import include
from django.urls import path
from . import views

app_name = 'webApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('', include('django.contrib.auth.urls')),
]

