from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenBlacklistView
from .views import UserLoginView, UserChangePasswordView, UserResetPasswordView, SendUserResetPasswordOTPView, ForgotPasswordView, LogoutView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='core/index.html')),
    path('login/', UserLoginView.as_view()),
    path('change-password/', UserChangePasswordView.as_view()),
    path('reset-password/', UserResetPasswordView.as_view()),
    path('reset-password/verify-otp/', SendUserResetPasswordOTPView.as_view()),
    path('reset-password/set/', ForgotPasswordView.as_view(), name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
