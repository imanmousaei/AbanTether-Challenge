from django.db import models
from django.utils.translation import gettext_lazy as _


class Coin(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Coin Name'))
    symbol = models.CharField(max_length=255, unique=True, verbose_name=_('Coin Symbol'))
    to_buy = models.FloatField(default=0, verbose_name=_('Residual coins that we need to buy when it exceeds 10'))
    price_in_usdt = models.FloatField(verbose_name=_('Coin Price in USDT'))
    
    def __str__(self):
        return self.symbol

class CoinBalance(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, verbose_name=_('Coin'))
    balance = models.FloatField(verbose_name=_('Coin Balance'))
    
    def __str__(self):
        return self.coin.symbol + ' ' + str(self.balance)