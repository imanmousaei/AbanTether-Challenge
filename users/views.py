import os
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from AbanTether.utils import *
from users.models import Customer
from users.serializers import CustomerSerializer
from exchange.models import CoinBalance


def body_parser(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return body
    

class RegisterView(APIView):
    def post(self, request):
        body = body_parser(request)
        phone_number = body.get('phone')
        first_name = body.get('first_name')
        last_name = body.get('last_name')
        username = body.get('username')

        user = User.objects.create(username=username, first_name=first_name, last_name=last_name)
        customer = Customer.objects.create(user=user, phone_number=phone_number)

        response = {
            'success': True,
        }
        return Response(response, status=status.HTTP_201_CREATED)
