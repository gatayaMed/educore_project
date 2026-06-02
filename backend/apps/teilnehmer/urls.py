"""
URL configuration for the Participant app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeilnehmerViewSet

router = DefaultRouter()
router.register(r'', TeilnehmerViewSet, basename='teilnehmer')

urlpatterns = [
    path('', include(router.urls)),
]