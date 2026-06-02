"""
URL configuration for the Enrollment app
"""

from django.urls import path
from .views import AnmeldungCreateView

urlpatterns = [
    path('', AnmeldungCreateView.as_view(), name='anmeldung-create'),
]