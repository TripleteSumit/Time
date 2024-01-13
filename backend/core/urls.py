from django.urls import path
from django.views.generic import TemplateView
from .views import UserLoginView
urlpatterns = [
    path('', TemplateView.as_view(template_name='core/index.html')),
    path('login/', UserLoginView.as_view()),
]
