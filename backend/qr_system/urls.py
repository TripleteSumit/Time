from django.urls import path
from .views import ClassListCreateView, GenerateQRCodeView

urlpatterns = [
    path('classes/', ClassListCreateView.as_view(), name='class-list-create'),
    path('generate-qr/<int:pk>/', GenerateQRCodeView.as_view(), name='generate-qr'),
]