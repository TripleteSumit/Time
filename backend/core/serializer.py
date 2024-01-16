import random
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from .models import User, ForgotPasswordOTP
from .email import EmailUtil
from datetime import timedelta
from django.utils import timezone


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


class UserRestPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attr):
        email = attr.get('email')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Provided email doesn't exist"})
        user = User.objects.get(email=email)

        # send mail data
        otp = random.randint(1000, 9999)
        if ForgotPasswordOTP.objects.filter(user=user.id).exists():
            forgot = ForgotPasswordOTP.objects.get(user_id=user.id)
            forgot.otp = otp
            forgot.created_at = timezone.now()
        else:
            forgot = ForgotPasswordOTP.objects.create(otp=otp, user_id=user.id)
        forgot.save()
        data = {"otp": otp, "mail": email}
        EmailUtil.send_mail(data)
        return attr


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

    def is_otp_expired(self, otp):
        expired_time = otp.created_at + timedelta(minutes=5)
        return timezone.now() > expired_time

    def validate(self, attrs):
        otp = attrs.get('otp')
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            return serializers.ValidationError({"email": "Email doesn't exist"})

        user_id = User.objects.get(email=email).id
        stored_otp = ForgotPasswordOTP.objects.get(user=user_id)
        if (otp != stored_otp.otp or self.is_otp_expired(stored_otp)):
            raise serializers.ValidationError(
                {"otp": "Entered OTP is either wrong or expired"})
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        pass1 = attrs.get('new_password')
        pass2 = attrs.get('confirm_password')
        email = self.context.get('email')
        if (pass1 != pass2):
            raise serializers.ValidationError(
                {"equality_error": "new password is not same as confirm password"})
        user = User.objects.get(email=email)
        old_password = user.password
        if check_password(pass1, old_password):
            raise serializers.ValidationError(
                {"new_password": "New password can not be same as old password."})
        user.set_password(pass1)
        user.save()
        return attrs
