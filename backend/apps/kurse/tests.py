"""
Tests for the Course model and API
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Kurs


class KursModelTest(TestCase):
    """Tests for the Course model."""
    
    def setUp(self):
        self.kurs = Kurs.objects.create(
            titel="Python Grundlagen",
            beschreibung="Einführung in Python",
            start_datum="2026-04-01",
            end_datum="2026-04-30",
            max_teilnehmer=2
        )
    
    def test_kurs_creation(self):
        """Test that a course can be created."""
        self.assertEqual(self.kurs.titel, "Python Grundlagen")
        self.assertEqual(self.kurs.max_teilnehmer, 2)
    
    def test_capacity_validation(self):
        """Test that capacity must be at least 1."""
        with self.assertRaises(ValidationError):
            kurs = Kurs(
                titel="Testkurs",
                max_teilnehmer=0,
                start_datum="2026-04-01",
                end_datum="2026-04-30"
            )
            kurs.full_clean()
    
    def test_date_validation(self):
        """Test that end date must be after start date."""
        kurs = Kurs(
            titel="Testkurs",
            max_teilnehmer=5,
            start_datum="2026-04-30",
            end_datum="2026-04-01"
        )
        
        with self.assertRaises(ValidationError) as context:
            kurs.full_clean()
        
        self.assertIn('end_datum', str(context.exception))
    
    def test_available_seats_property(self):
        """Test available_seats calculation."""
        self.assertEqual(self.kurs.verfuegbare_plaetze, 2)
        self.assertFalse(self.kurs.ist_voll)


class KursAPITest(TestCase):
    """Tests for the Course API endpoints."""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        
        # API client with authentication
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        
        # Create test course
        self.kurs = Kurs.objects.create(
            titel="Python Testkurs",
            beschreibung="Testbeschreibung",
            start_datum="2026-04-01",
            end_datum="2026-04-30",
            max_teilnehmer=10
        )
    
    def test_get_courses_list(self):
        """Test GET /api/kurse/ returns list of courses."""
        response = self.client.get('/api/kurse/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
    
    def test_get_course_detail(self):
        """Test GET /api/kurse/{id}/ returns course details."""
        response = self.client.get(f'/api/kurse/{self.kurs.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titel'], "Python Testkurs")
        self.assertIn('anzahl_anmeldungen', response.data)
    
    def test_get_nonexistent_course(self):
        """Test GET /api/kurse/999/ returns 404."""
        response = self.client.get('/api/kurse/999/')
        self.assertEqual(response.status_code, 404)
    
    def test_unauthenticated_access(self):
        """Test that unauthenticated requests are rejected."""
        client = APIClient()
        response = client.get('/api/kurse/')
        self.assertEqual(response.status_code, 401)