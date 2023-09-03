from django.db import models
from django.utils.translation import ugettext_lazy as _


class Coin(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Coin Name'))
    symbol = models.CharField(max_length=255, verbose_name=_('Coin Symbol'))
    to_buy = models.FloatField(verbose_name=_('Residual coins that we need to buy when it exceeds 10'))
    price = models.FloatField(verbose_name=_('Coin Price in USD'))
