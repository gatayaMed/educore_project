"""
Participant model for the educore platform
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class Teilnehmer(models.Model):
    """
    Model representing a participant/customer.
    """
    vorname = models.CharField(max_length=50, verbose_name="Vorname")
    nachname = models.CharField(max_length=50, verbose_name="Nachname")
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name="E-Mail",
        db_index=True
    )
    telefon = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    aktualisiert_am = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    
    class Meta:
        verbose_name = "Teilnehmer"
        verbose_name_plural = "Teilnehmer"
        ordering = ['nachname', 'vorname']
        indexes = [
            models.Index(fields=['nachname', 'vorname']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.nachname}, {self.vorname} ({self.email})"
    
    @property
    def vollstaendiger_name(self):
        """Return the full name of the participant."""
        return f"{self.vorname} {self.nachname}"
    
    def clean(self):
        """Validate the model before saving."""
        if not self.vorname or not self.nachname:
            raise ValidationError("Vor- und Nachname sind Pflichtfelder.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)