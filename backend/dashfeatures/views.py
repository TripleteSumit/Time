from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Teacher
from .serializer import TeacherProfileSerializer
from django.conf import settings
from django.shortcuts import get_object_or_404


class UserProfileView(APIView):
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile_data = get_object_or_404(
            Teacher, user_id=request.user.id)
        serializer = TeacherProfileSerializer(
            user_profile_data, context={"user": request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)
