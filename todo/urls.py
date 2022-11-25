from django.urls import path
from . import views


app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index),
    path("login", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("logout", views.logout_request, name= "logout"),
    #path("deneme", views.todo_index)
] 
