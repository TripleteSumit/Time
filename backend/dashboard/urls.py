"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

admin.site.site_header = 'Time Kit'
admin.site.index_title = 'Admin'

urlpatterns = [
    # path('', include('core.urls')), --> this path showcase the authentication ui.
    path('auth/', include('core.urls')),
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('profile/', include('dashfeatures.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/test/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='schema-test'),
    path('', SpectacularRedocView.as_view(url_name='schema')),
    path('api/', include('qr_system.urls'))

]
