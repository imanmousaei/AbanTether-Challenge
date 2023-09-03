from django.urls import path

from .views import *

app_name = 'exchange'


urlpatterns = [
    path('place_order', PlaceOrderView.as_view(), name='place_order'),
]
