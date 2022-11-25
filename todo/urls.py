from django.urls import path
from . import views


app_name = 'todo'

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path("register", views.register_request, name="register")
]
