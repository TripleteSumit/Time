from django.urls import path
from django.views.generic import TemplateView
from .views import UserLoginView, UserChangePasswordView, UserResetPasswordView, SendUserResetPasswordOTPView, ForgotPasswordView

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/index.html')),
    path('auth/login/', UserLoginView.as_view()),
    path('change-password/', UserChangePasswordView.as_view()),
    path('reset-password/', UserResetPasswordView.as_view()),
    path('reset-password/verify-otp/',
         SendUserResetPasswordOTPView.as_view()),
    path('reset-password/set/', ForgotPasswordView.as_view()),
]
