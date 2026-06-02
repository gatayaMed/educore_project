"""
URL configuration for the Course app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KursViewSet

router = DefaultRouter()
router.register(r'', KursViewSet, basename='kurs')

urlpatterns = [
    path('', include(router.urls)),
]