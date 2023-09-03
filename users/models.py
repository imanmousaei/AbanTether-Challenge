from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('Phone Number'))
    national_id = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Melli Code'))
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('City'))
    level = models.PositiveIntegerField(default=1, verbose_name=_('Authentication Level'))

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return self.user.first_name + ' ' + self.user.last_name
        return self.user.username

    class Meta:
        verbose_name_plural = 'Customers'
