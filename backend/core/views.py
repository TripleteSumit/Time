from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializer import UserLoginSerializer, UserChangePasswordSerializer, UserRestPasswordSerializer


def get_token(user):
    refresh_token = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh_token),
        'access': str(refresh_token.access_token),
    }


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'field error': ["Check you username and pasword and try again"]}, status=status.HTTP_404_NOT_FOUND)
        else:
            token = get_token(user)
            return Response({"token": token, "msg": "Login successfull"}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"msg": "Password Chaged Successfully."}, status=status.HTTP_200_OK)


class UserResetPasswordView(APIView):

    def post(self, request):
        serializer = UserRestPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"msg": "OTP is send to you email.", "data": serializer.data}, status=status.HTTP_200_OK)
