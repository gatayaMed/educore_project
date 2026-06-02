"""
Course model for the educore platform
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Kurs(models.Model):
    """
    Model representing a course.
    """  
    titel = models.CharField(max_length=200, verbose_name="Titel")
    beschreibung = models.TextField(blank=True, verbose_name="Beschreibung")
    start_datum = models.DateField(verbose_name="Startdatum")
    end_datum = models.DateField(verbose_name="Enddatum")
    max_teilnehmer = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Maximale Teilnehmerzahl"
    )
    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    aktualisiert_am = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    
    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurse"
        ordering = ['-erstellt_am']
        indexes = [
            models.Index(fields=['titel']),
            models.Index(fields=['start_datum']),
        ]
    
    def __str__(self):
        return f"{self.titel} (max. {self.max_teilnehmer} Plätze)"
    
    @property
    def verfuegbare_plaetze(self):
        """
        Calculate the number of available seats.
        Only counts active enrollments.
        """
        aktive_anmeldungen = self.anmeldungen.filter(status='angemeldet').count()
        return self.max_teilnehmer - aktive_anmeldungen
    
    @property
    def anzahl_anmeldungen(self):
        """Return the number of active enrollments."""
        return self.anmeldungen.filter(status='angemeldet').count()
    
    @property
    def ist_voll(self):
        """Check if the course is full."""
        return self.verfuegbare_plaetze <= 0
    
    def clean(self):
        """Validate the model before saving."""
        if self.start_datum and self.end_datum and self.start_datum > self.end_datum:
            raise ValidationError({
                'end_datum': "Das Enddatum muss nach dem Startdatum liegen."
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)