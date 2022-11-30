from django.urls import path
from . import views


app_name = 'todo'

urlpatterns = [
    path('', views.index),
    path('index', views.index, name='index'),
    path("login", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("logout", views.logout_request, name= "logout"),
    #path("deneme", views.denemelere)
] 
