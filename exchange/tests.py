from django.test import TestCase, Client

from exchange.models import *
from users.models import *


class CoinBalanceAPITestCase(TestCase):
    def setUp(self):
        usdt = Coin.objects.create(name='Tether', symbol='USDT', price_in_usdt=1)
        btc = Coin.objects.create(name='Bitcoin', symbol='BTC', price_in_usdt=25866)
        shitcoin = Coin.objects.create(name='Shitcoin', symbol='STC', price_in_usdt=0.005)

        user = User.objects.create(first_name='Iman', last_name='Mousaei', username='imanmousaei')
        coin_balance = CoinBalance.objects.create(coin=usdt, balance=10000000)
        Customer.objects.create(user=user, coin_balance=coin_balance)
                
        self.client = Client()
    
    def test_create_coin_balance(self):
        request = {
            'symbol': 'STC',
            'amount': 100000,
            'username': 'imanmousaei',
        }
        
        response = self.client.post('/api/v1/exchange/place_order', request)
        
        # assert that the request was successful (HTTP 201 status code)
        self.assertEqual(response.status_code, 201)
