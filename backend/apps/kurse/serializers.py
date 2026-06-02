"""
Serializers for the Course model
"""

from rest_framework import serializers
from .models import Kurs


class KursSerializer(serializers.ModelSerializer):
    """Serializer for Course model with computed fields."""
    
    verfuegbare_plaetze = serializers.IntegerField(read_only=True)
    ist_voll = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Kurs
        fields = ['id', 'titel', 'beschreibung', 'start_datum', 'end_datum',
                 'max_teilnehmer', 'verfuegbare_plaetze', 'ist_voll',
                 'erstellt_am', 'aktualisiert_am']
        read_only_fields = ['id', 'erstellt_am', 'aktualisiert_am']


class KursDetailSerializer(KursSerializer):
    """Detailed Course serializer with additional enrollment count."""
    
    anzahl_anmeldungen = serializers.IntegerField(read_only=True)
    
    class Meta(KursSerializer.Meta):
        fields = KursSerializer.Meta.fields + ['anzahl_anmeldungen']