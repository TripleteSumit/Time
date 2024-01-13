from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(style={'input_type': 'password'})
