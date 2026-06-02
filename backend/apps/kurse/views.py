"""
Views for the Course API endpoints
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Kurs
from .serializers import KursSerializer, KursDetailSerializer


class KursViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for courses (read-only as per requirements).
    
    Provides:
    - GET /api/kurse/ - List all courses
    - GET /api/kurse/{id}/ - Get course details
    """
    
    queryset = Kurs.objects.all()
    serializer_class = KursSerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get course details with full information including enrollment count.
        """
        instance = self.get_object()
        serializer = KursDetailSerializer(instance)
        return Response(serializer.data)
    
    def get_queryset(self):
        """
        Optionally filter courses by date or search term.
        """
        queryset = super().get_queryset()
        
        # Filter by active courses (start date in future)
        from django.utils import timezone
        only_future = self.request.query_params.get('only_future')
        if only_future and only_future.lower() == 'true':
            queryset = queryset.filter(start_datum__gte=timezone.now().date())
        
        # Search by title
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(titel__icontains=search)
        
        return queryset