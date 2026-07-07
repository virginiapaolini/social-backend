"""
URL configuration for the socialAPI project.

The `urlpatterns` list routes URLs to views. For more info please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

# uso interfaccia web di Django REST Framework!!!

@api_view(['GET'])
@permission_classes([AllowAny])
def api_home_view(request, format=None):
    """
    Benvenut* nella Social Media REST API!
    questa è la pagina principale del back-end... sotto trovi una lista degli endpoint principali disponibili
    """
    return Response({
        "info": {
            "project_name": "Social Media REST API",
            "description": "Progetto finale per il corso di Back-end PPM 2026.",
            "status": "ONLINE",
            "version": "1.0.0"
        },
        "endpoints_disponibili": {
            "autenticazione_login": reverse('token_obtain_pair', request=request, format=format),
            "lista_utenti": reverse('user-list', request=request, format=format),
            "lista_post": reverse('post-list', request=request, format=format),
            "feed_personalizzato": reverse('feed-timeline', request=request, format=format)
        }
    })


urlpatterns = [
    path('', api_home_view, name='api-home'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
]