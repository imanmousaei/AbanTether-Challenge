from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Customer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        # exclude = ('password', )
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('id',)


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'
        # exclude = ('self.user.password', )
        read_only_fields = ('id',)
        depth = 1
