"""
URL configuration for educore project
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from rest_framework.authtoken import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
    
    # API
    path('api/', include('apps.api_urls')),
    
    # Swagger/OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve media files in production (required for uploaded files)
re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),