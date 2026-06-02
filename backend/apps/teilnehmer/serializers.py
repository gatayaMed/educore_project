"""
Serializers for the Participant model
"""

from rest_framework import serializers
from .models import Teilnehmer


class TeilnehmerSerializer(serializers.ModelSerializer):
    """Serializer for Participant model."""
    
    vollstaendiger_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Teilnehmer
        fields = ['id', 'vorname', 'nachname', 'vollstaendiger_name', 
                 'email', 'telefon', 'erstellt_am', 'aktualisiert_am']
        read_only_fields = ['id', 'erstellt_am', 'aktualisiert_am']


class TeilnehmerCreateSerializer(serializers.Serializer):
    """Serializer for creating a participant from enrollment data."""
    
    vorname = serializers.CharField(max_length=50)
    nachname = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    telefon = serializers.CharField(max_length=20, required=False, allow_blank=True)