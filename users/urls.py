from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('students', StudentView.as_view(), name='register_user'),
    path('complete_profile/<phone_number>', StudentView.as_view(), name='register_user'),
    path('verify_OTP', VerifyUser.as_view(), name='verify_user'),

]