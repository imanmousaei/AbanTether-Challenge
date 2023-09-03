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


def body_parser(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return body
    

class CustomerView(APIView):
    def post(self, request):
        body = body_parser(request)
        phone_number = body.get('phone')
        first_name = body.get('first_name')
        last_name = body.get('last_name')

        try:
            customer = Customer.objects.get(phone_number=phone_number)
        except:
            user = User(username=phone_number, first_name=first_name, last_name=last_name)
            user.save()
            customer = Customer(user=user, phone_number=phone_number)
            customer.save()

        response = {
            "customer": CustomerSerializer(customer).data,
        }
        return Response(response, status=status.HTTP_201_CREATED)


    def get(self, request):
        customers = Customer.objects.all()

        response = {
            "customers": CustomerSerializer(customers, many=True).data,
        }
        return Response(response, status=status.HTTP_200_OK)


    def patch(self, request, phone_number):
        body = body_parser(request)
        customer = Customer.objects.get(phone_number=phone_number)
        user = customer.user
        serializer = CustomerSerializer(customer, data=request.data, partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            context = {
                'success': True,
                'message': 'Customer Updated Successfully'
            }
            first_name = body.get('first_name')
            last_name = body.get('last_name')
            if first_name and last_name:
                user.first_name = first_name
                user.last_name = last_name
            user.save()

            return Response(context, status=status.HTTP_201_CREATED)

        print(serializer.errors)

        context = {
            'success': False,
            'message': 'Wrong Parameters'
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


class VerifyUser(APIView):
    def post(self, request):
        phone_number = request.POST.get('phone')
        otp = request.POST.get('otp')

        customer = Customer.objects.get(phone_number=phone_number)

        if otp == customer.otp:
            customer.otp = 'True'
            customer.save()
            success = True
        else:
            success = False

        response = {
            'success': success
        }
        return Response(response, status=status.HTTP_200_OK)


def fun(request):
    # print('here')
    send_mail(
        subject='here',
        message='self.text',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['imanmousaei1379@gmail.com'],
        fail_silently=False,
    )
    # print('here2')
    return HttpResponse('here')

