"""
Tests for the Participant model
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Teilnehmer


class TeilnehmerModelTest(TestCase):
    """Tests for the Participant model."""
    
    def setUp(self):
        self.teilnehmer = Teilnehmer.objects.create(
            vorname="Max",
            nachname="Mustermann",
            email="max@test.de",
            telefon="0123-456789"
        )
    
    def test_participant_creation(self):
        """Test that a participant can be created."""
        self.assertEqual(self.teilnehmer.vorname, "Max")
        self.assertEqual(self.teilnehmer.nachname, "Mustermann")
        self.assertEqual(self.teilnehmer.email, "max@test.de")
    
    def test_email_uniqueness(self):
        """Test that email must be unique."""
        with self.assertRaises(Exception):
            Teilnehmer.objects.create(
                vorname="Anna",
                nachname="Schmidt",
                email="max@test.de"  # Duplicate email
            )
    
    def test_required_fields(self):
        """Test that vorname and nachname are required."""
        teilnehmer = Teilnehmer(
            vorname="",
            nachname="",
            email="test@test.de"
        )
        
        with self.assertRaises(ValidationError):
            teilnehmer.full_clean()
    
    def test_full_name_property(self):
        """Test the full_name property."""
        self.assertEqual(
            self.teilnehmer.vollstaendiger_name,
            "Max Mustermann"
        )