"""
Serializers for the Enrollment model
"""

from rest_framework import serializers
from .models import Anmeldung
from apps.kurse.serializers import KursSerializer
from apps.teilnehmer.serializers import TeilnehmerSerializer


class AnmeldungSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model with nested data."""
    
    kurs_titel = serializers.CharField(source='kurs.titel', read_only=True)
    teilnehmer_name = serializers.CharField(
        source='teilnehmer.vollstaendiger_name', 
        read_only=True
    )
    
    class Meta:
        model = Anmeldung
        fields = ['id', 'kurs', 'kurs_titel', 'teilnehmer', 'teilnehmer_name',
                 'anmeldedatum', 'status']
        read_only_fields = ['id', 'anmeldedatum', 'status']


class AnmeldungCreateSerializer(serializers.Serializer):
    """
    Serializer for creating a new enrollment.
    """
    kurs = serializers.IntegerField()
    vorname = serializers.CharField(max_length=50)
    nachname = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    telefon = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    def validate_kurs(self, value):
        """Validate that the course exists and has capacity."""
        from educore_backend.apps.kurse.models import Kurs
        
        try:
            kurs = Kurs.objects.get(id=value)
        except Kurs.DoesNotExist:
            raise serializers.ValidationError("Der angegebene Kurs existiert nicht.")
        
        if kurs.ist_voll:
            raise serializers.ValidationError(
                f"Der Kurs '{kurs.titel}' ist bereits ausgebucht."
            )
        
        return value