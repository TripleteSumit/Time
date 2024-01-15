from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from .models import User


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(style={'input_type': 'password'})


class UserChangePasswordSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    newpassword = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    confirmpassword = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        old_pass = attrs.get('oldpassword')
        user = self.context['user']
        user_obj = User.objects.get(pk=user.id)
        if not check_password(old_pass, user_obj.password):
            raise serializers.ValidationError({"old_pass":
                                               "Password is not correct. Try again."})

        pass1 = attrs.get('newpassword')
        pass2 = attrs.get('confirmpassword')

        if pass1 != pass2:
            raise serializers.ValidationError({"password_missmatch":
                                               "password and confirm password doesn't match"})

        if check_password(pass1, user_obj.password):
            raise serializers.ValidationError({"new_password":
                                               "new password must not be same as old password"})

        user.set_password(pass1)
        user.save()
        return attrs
