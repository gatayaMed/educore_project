"""
Views for the Participant model
"""
from django.db import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Teilnehmer
from .serializers import TeilnehmerSerializer


class TeilnehmerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for participants.
    
    Provides full CRUD operations for participants.
    """
    
    queryset = Teilnehmer.objects.all()
    serializer_class = TeilnehmerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Optionally filter participants by search term.
        """
        queryset = super().get_queryset()
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(vorname__icontains=search) |
                models.Q(nachname__icontains=search) |
                models.Q(email__icontains=search)
            )
        
        return queryset