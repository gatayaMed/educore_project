"""
Central API URL configuration
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.kurse.views import KursViewSet
from apps.anmeldungen.views import AnmeldungCreateView

# Router for ViewSets
router = DefaultRouter()
router.register(r'kurse', KursViewSet, basename='kurs')

urlpatterns = [
    # Course endpoints (read-only)
    path('', include(router.urls)),
    
    # Enrollment endpoint
    path('anmeldungen/', AnmeldungCreateView.as_view(), name='anmeldung-create'),
]