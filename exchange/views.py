import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from exchange import consts
from exchange.models import *
from users.models import *


FIRST_TIME = False

class PlaceOrderView(APIView):
    def get(self, request):
        print('hi')
        return Response({}, status.HTTP_200_OK)

    def post(self, request):
        # used for TEST
        if FIRST_TIME == True:
            usdt = Coin.objects.create(name='Tether', symbol='USDT', price_in_usdt=1)
            btc = Coin.objects.create(name='Bitcoin', symbol='BTC', price_in_usdt=25866)

            user = User.objects.create(first_name='Iman', last_name='Mousaei', username='imanmousaei')
            coin_balance = CoinBalance.objects.create(coin=usdt, balance=10000000)
            Customer.objects.create(user=user, coin_balance=coin_balance)
            
        body = request.POST
        
        symbol = body.get('symbol')
        amount = float(body.get('amount'))
        username = body.get('username')
        
        coin = Coin.objects.get(symbol=symbol)
        user = User.objects.get(username=username)
        
        customer = user.customer
        price_in_usdt = coin.price_in_usdt
            
        # atomic is used to either do them all, or not do them all
        with transaction.atomic():
            # select_for_update is used to lock rows until end of transaction
            user_base_pair = CoinBalance.objects.select_for_update().get(customer=customer, coin__symbol=consts.base_pair)
            amount_in_usdt = price_in_usdt * amount
            
            if user_base_pair.balance < amount_in_usdt:
                response = {
                    'success': False,
                    'msg': 'Insufficient Balance',
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)

            # if balance is enough:
            user_base_pair.balance -= amount_in_usdt
            user_base_pair.save()
            
            try:
                user_coin_balance = CoinBalance.objects.select_for_update().get(customer=customer, coin__symbol=symbol)
            except:
                # if does not exist:
                user_coin_balance = CoinBalance.objects.select_for_update().create(customer=customer, coin=coin, balance=0)
                
            user_coin_balance.balance += amount
            user_coin_balance.save()


            response = {
                'success': True,
                'error': 'Transaction was successful',
            }
            return Response(response, status.HTTP_201_CREATED)
