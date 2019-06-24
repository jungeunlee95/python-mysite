from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('joinform', views.joinform, name='joinform'),
    path('joinsuccess', views.joinsuccess, name='joinsuccess'),
    path('join', views.join, name='join'),

    path('api/checkemail', views.checkemail, name='checkemail'),

    path('loginform', views.loginform, name='loginform'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('updateform', views.updateform, name='updateform'),
    path('update', views.update, name='update'),
]