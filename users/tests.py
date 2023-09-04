from django.test import TestCase
from tastypie.test import ResourceTestCase

from .models import *
from exchange.models import *


class PlaceOrderTestCase(ResourceTestCase):
    def setUp(self):
        usdt = Coin.objects.create(name='Tether', symbol='USDT', price_in_usdt=1)
        btc = Coin.objects.create(name='Bitcoin', symbol='BTC', price_in_usdt=25866)

        user = User.objects.create(first_name='Iman', last_name='Mousaei', username='imanmousaei')
        coin_balance = CoinBalance.objects.create(coin=usdt, balance=1000)
        Customer.objects.create(user=user, coin_balance=coin_balance)
        
    def test_correct_order(self):
        lion = Coin.objects.get(name="lion")
        response = self.api_client.post('/api/v1/exchange/place_order', format='json')
        print(response)

        self.assertEqual(response., 'The cat says "meow"')