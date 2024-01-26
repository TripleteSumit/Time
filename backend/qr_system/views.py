from django.shortcuts import render

# Create your views here.

import qrcode
from rest_framework import generics, status
from rest_framework.response import Response
from  .models import Class
from .serializers import ClassSerializer

class ClassListCreateView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class GenerateQRCodeView(generics.RetrieveAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        qr_code_data = f"Class: {instance.name}, Date: {instance.date}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        response = Response(status=status.HTTP_200_OK)
        response.accepted_renderer = img
        response.accepted_media_type = 'image/png'
        response.renderer_context = {}

        return response

