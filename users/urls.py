from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register_user'),
]