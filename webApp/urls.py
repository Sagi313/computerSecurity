from django.conf.urls import include
from django.urls import path
from . import views

app_name = 'webApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('logout/', views.logout_user, name="logout"),
    path('password_changing/', views.password_change, name='password_change'),
]

