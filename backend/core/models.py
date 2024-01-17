from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)


class ForgotPasswordOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
