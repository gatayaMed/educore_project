"""
Views for the Enrollment API endpoints
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Anmeldung
from .serializers import AnmeldungSerializer, AnmeldungCreateSerializer
from apps.kurse.models import Kurs
from apps.teilnehmer.models import Teilnehmer


class AnmeldungCreateView(APIView):
    """
    View for creating a new enrollment.
    
    POST /api/anmeldungen/
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Create a new enrollment.
        
        Steps:
        1. Validate input data
        2. Check if course exists
        3. Find or create participant
        4. Check for duplicate enrollment
        5. Check course capacity
        6. Create enrollment
        7. Return response
        """
        
        # Validate input
        serializer = AnmeldungCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Ungültige Eingabe', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = serializer.validated_data
        
        # Get course
        kurs = get_object_or_404(Kurs, id=data['kurs'])
        
        # Check capacity again (in case it changed)
        if kurs.ist_voll:
            return Response(
                {'error': f'Der Kurs "{kurs.titel}" ist bereits ausgebucht.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find or create participant
        teilnehmer, created = Teilnehmer.objects.get_or_create(
            email=data['email'],
            defaults={
                'vorname': data['vorname'],
                'nachname': data['nachname'],
                'telefon': data.get('telefon', '')
            }
        )
        
        # Check for duplicate active enrollment
        if Anmeldung.objects.filter(
            kurs=kurs,
            teilnehmer=teilnehmer,
            status='angemeldet'
        ).exists():
            return Response(
                {'error': 'Teilnehmer ist bereits zu diesem Kurs angemeldet.'},
                status=status.HTTP_409_CONFLICT
            )
        
        # Create enrollment
        anmeldung = Anmeldung.objects.create(
            kurs=kurs,
            teilnehmer=teilnehmer,
            status='angemeldet'
        )
        
        # Return response
        response_serializer = AnmeldungSerializer(anmeldung)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )