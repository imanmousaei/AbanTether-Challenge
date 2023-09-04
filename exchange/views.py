import json

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction

from exchange.models import Coin
from exchange import consts



def body_parser(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return body


class PlaceOrderView(APIView):
    def post(self, request):
        body = body_parser(request)
        
        symbol = body.get('symbol')
        amount = body.get('amount')
        user_id = body.get('user_id')
        
        coin = Coin.objects.get(symbol=symbol)
        user = User.objects.get(id=user_id)
        
        price_in_usdt = coin.price_in_usdt
            
        # select_for_update is used to lock rows until end of transaction
        user_base_pair = user.coin_balance.select_for_update().get(symbol=consts.base_pair)
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
        
        user_coin_balance = user.coin_balance.select_for_update().get(symbol=symbol)
        user_coin_balance.balance += amount
        user_coin_balance.save()


        response = {
            'success': True,
            'error': 'Transaction was successful',
        }
        return Response(response, status.HTTP_201_CREATED)
