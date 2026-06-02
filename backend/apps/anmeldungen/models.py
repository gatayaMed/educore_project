"""
Enrollment model for the educore platform
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Anmeldung(models.Model):
    """
    Model representing a course enrollment.
    """
    
    STATUS_CHOICES = [
        ('angemeldet', 'Angemeldet'),
        ('storniert', 'Storniert'),
    ]
    
    kurs = models.ForeignKey(
        'kurse.Kurs',
        on_delete=models.CASCADE,
        related_name='anmeldungen',
        verbose_name="Kurs"
    )
    teilnehmer = models.ForeignKey(
        'teilnehmer.Teilnehmer',
        on_delete=models.CASCADE,
        related_name='anmeldungen',
        verbose_name="Teilnehmer"
    )
    anmeldedatum = models.DateTimeField(
        default=timezone.now,
        verbose_name="Anmeldedatum"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='angemeldet',
        verbose_name="Status"
    )
    
    class Meta:
        verbose_name = "Anmeldung"
        verbose_name_plural = "Anmeldungen"
        unique_together = ['kurs', 'teilnehmer']
        indexes = [
            models.Index(fields=['kurs', 'status']),
            models.Index(fields=['teilnehmer']),
        ]
        ordering = ['-anmeldedatum']
    
    def __str__(self):
        return f"{self.teilnehmer} → {self.kurs} ({self.get_status_display()})"
    
    def clean(self):
        """Validate business rules before saving."""
        if self.status == 'angemeldet':
            self._prevent_duplicate_enrollment()
            self._check_course_capacity()
    
    def _prevent_duplicate_enrollment(self):
        """Prevent duplicate active enrollments."""
        existing = Anmeldung.objects.filter(
            kurs=self.kurs,
            teilnehmer=self.teilnehmer,
            status='angemeldet'
        ).exclude(pk=self.pk)
        
        if existing.exists():
            raise ValidationError(
                f"Teilnehmer {self.teilnehmer.vollstaendiger_name} ist bereits "
                f"zum Kurs '{self.kurs.titel}' angemeldet."
            )
    
    def _check_course_capacity(self):
        """Check if the course has available seats."""
        if self.kurs.ist_voll:
            raise ValidationError(
                f"Der Kurs '{self.kurs.titel}' ist bereits ausgebucht "
                f"(max. {self.kurs.max_teilnehmer} Teilnehmer)."
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def cancel(self):
        """Cancel the enrollment (keeps the record)."""
        if self.status == 'storniert':
            raise ValidationError("Diese Anmeldung ist bereits storniert.")
        
        self.status = 'storniert'
        self.save(update_fields=['status'])
    
    @property
    def is_active(self):
        """Check if the enrollment is active."""
        return self.status == 'angemeldet'