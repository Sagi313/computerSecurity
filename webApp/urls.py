from django.conf.urls import include
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy



app_name = 'webApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('search_results/', views.search_results, name='search_results'),
    path('register/', views.register, name='register'),
    #path('login/', auth_views.LoginView.as_view()),
    path('logout/', views.logout_user, name="logout"),
    path('chat/', views.chat, name='chat'),
    path('about/', views.about, name='about'),
    path('password_changing/', views.changepasswordsform.as_view(template_name='registration/change-password.html', success_url=reverse_lazy('webApp:password_success')), name='password_change'),
    path('password_change_successfully/', views.password_success, name='password_success'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/reset_password.html', email_template_name ='registration/password_reset_email.txt',success_url=reverse_lazy('webApp:password_reset_done')), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html', success_url=reverse_lazy('webApp:password_reset_complete')), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),
    path('login/', views.loginPage, name='login'),
]

