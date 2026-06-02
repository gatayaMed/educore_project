"""
Tests for the Enrollment model and API
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from educore_backend.apps.kurse.models import Kurs
from educore_backend.apps.teilnehmer.models import Teilnehmer
from .models import Anmeldung


class AnmeldungModelTest(TestCase):
    """Tests for the Enrollment model."""
    
    def setUp(self):
        self.kurs = Kurs.objects.create(
            titel="Python Testkurs",
            max_teilnehmer=2,
            start_datum="2026-04-01",
            end_datum="2026-04-30"
        )
        self.teilnehmer1 = Teilnehmer.objects.create(
            vorname="Max",
            nachname="Mustermann",
            email="max@test.de"
        )
        self.teilnehmer2 = Teilnehmer.objects.create(
            vorname="Anna",
            nachname="Schmidt",
            email="anna@test.de"
        )
    
    def test_successful_enrollment(self):
        """Test that a participant can enroll in a course."""
        anmeldung = Anmeldung.objects.create(
            kurs=self.kurs,
            teilnehmer=self.teilnehmer1
        )
        
        self.assertEqual(anmeldung.status, 'angemeldet')
        self.assertIsNotNone(anmeldung.anmeldedatum)
    
    def test_capacity_check(self):
        """Test that enrollment fails when course is full."""
        # First enrollment
        Anmeldung.objects.create(
            kurs=self.kurs,
            teilnehmer=self.teilnehmer1
        )
        
        # Second enrollment
        Anmeldung.objects.create(
            kurs=self.kurs,
            teilnehmer=self.teilnehmer2
        )
        
        # Third participant
        teilnehmer3 = Teilnehmer.objects.create(
            vorname="Peter",
            nachname="Müller",
            email="peter@test.de"
        )
        
        # Third enrollment should fail
        anmeldung3 = Anmeldung(
            kurs=self.kurs,
            teilnehmer=teilnehmer3
        )
        
        with self.assertRaises(ValidationError) as context:
            anmeldung3.save()
        
        self.assertIn("ausgebucht", str(context.exception))
    
    def test_duplicate_enrollment_check(self):
        """Test that duplicate enrollment is prevented."""
        # First enrollment
        Anmeldung.objects.create(
            kurs=self.kurs,
            teilnehmer=self.teilnehmer1
        )
        
        # Second enrollment with same participant
        anmeldung2 = Anmeldung(
            kurs=self.kurs,
            teilnehmer=self.teilnehmer1
        )
        
        with self.assertRaises(ValidationError) as context:
            anmeldung2.save()
        
        self.assertIn("bereits", str(context.exception))
    
    def test_cancel_enrollment(self):
        """Test that enrollment can be cancelled."""
        anmeldung = Anmeldung.objects.create(
            kurs=self.kurs,
            teilnehmer=self.teilnehmer1
        )
        
        anmeldung.cancel()
        
        self.assertEqual(anmeldung.status, 'storniert')
    
    def test_cancelled_enrollment_frees_capacity(self):
        """Test that cancelled enrollment frees a seat."""
        # Create two enrollments to fill the course
        Anmeldung.objects.create(
            kurs=self.kurs,
            teilnehmer=self.teilnehmer1
        )
        
        anmeldung2 = Anmeldung.objects.create(
            kurs=self.kurs,
            teilnehmer=self.teilnehmer2
        )
        
        # Course should be full
        self.assertTrue(self.kurs.ist_voll)
        
        # Cancel one enrollment
        anmeldung2.cancel()
        
        # Course should have available seats
        self.assertFalse(self.kurs.ist_voll)
        self.assertEqual(self.kurs.verfuegbare_plaetze, 1)


class AnmeldungAPITest(TestCase):
    """Tests for the Enrollment API endpoint."""
    
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
            max_teilnehmer=2,
            start_datum="2026-04-01",
            end_datum="2026-04-30"
        )
    
    def test_successful_enrollment_api(self):
        """Test POST /api/anmeldungen/ with valid data."""
        response = self.client.post('/api/anmeldungen/', {
            'kurs': self.kurs.id,
            'vorname': 'Max',
            'nachname': 'Mustermann',
            'email': 'max@test.de',
            'telefon': '0123-456789'
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'angemeldet')
        self.assertEqual(response.data['kurs_titel'], self.kurs.titel)
    
    def test_enrollment_when_course_full_api(self):
        """Test enrollment fails when course is full."""
        # Fill the course with two enrollments
        for i in range(2):
            self.client.post('/api/anmeldungen/', {
                'kurs': self.kurs.id,
                'vorname': f'Vorname{i}',
                'nachname': f'Nachname{i}',
                'email': f'test{i}@test.de'
            })
        
        # Third enrollment should fail
        response = self.client.post('/api/anmeldungen/', {
            'kurs': self.kurs.id,
            'vorname': 'Peter',
            'nachname': 'Müller',
            'email': 'peter@test.de'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('ausgebucht', response.data['error']['message'])
    
    def test_duplicate_enrollment_api(self):
        """Test duplicate enrollment returns 409 Conflict."""
        # First enrollment
        self.client.post('/api/anmeldungen/', {
            'kurs': self.kurs.id,
            'vorname': 'Max',
            'nachname': 'Mustermann',
            'email': 'max@test.de'
        })
        
        # Second enrollment with same participant
        response = self.client.post('/api/anmeldungen/', {
            'kurs': self.kurs.id,
            'vorname': 'Max',
            'nachname': 'Mustermann',
            'email': 'max@test.de'
        })
        
        self.assertEqual(response.status_code, 409)
        self.assertIn('bereits', response.data['error']['message'])
    
    def test_nonexistent_course_api(self):
        """Test enrollment with non-existent course returns 404."""
        response = self.client.post('/api/anmeldungen/', {
            'kurs': 9999,
            'vorname': 'Max',
            'nachname': 'Mustermann',
            'email': 'max@test.de'
        })
        
        self.assertEqual(response.status_code, 404)
    
    def test_unauthenticated_enrollment(self):
        """Test that unauthenticated requests are rejected."""
        client = APIClient()
        response = client.post('/api/anmeldungen/', {
            'kurs': self.kurs.id,
            'vorname': 'Max',
            'nachname': 'Mustermann',
            'email': 'max@test.de'
        })
        
        self.assertEqual(response.status_code, 401)
    
    def test_missing_required_fields(self):
        """Test enrollment with missing fields returns 400."""
        response = self.client.post('/api/anmeldungen/', {
            'kurs': self.kurs.id,
            'vorname': 'Max'
            # Missing nachname and email
        })
        
        self.assertEqual(response.status_code, 400)