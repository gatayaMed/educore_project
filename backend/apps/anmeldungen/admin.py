"""
Admin configuration for the Enrollment model
"""

from django.contrib import admin
from .models import Anmeldung


@admin.register(Anmeldung)
class AnmeldungAdmin(admin.ModelAdmin):
    list_display = ['id', 'kurs', 'teilnehmer', 'anmeldedatum', 'status']
    list_filter = ['status', 'kurs']
    search_fields = ['kurs__titel', 'teilnehmer__email', 'teilnehmer__nachname']
    readonly_fields = ['anmeldedatum']
    actions = ['cancel_enrollments']
    
    def cancel_enrollments(self, request, queryset):
        """Admin action to cancel multiple enrollments."""
        for enrollment in queryset:
            if enrollment.status == 'angemeldet':
                enrollment.cancel()
        self.message_user(request, f"{queryset.count()} Anmeldungen wurden storniert.")
    
    cancel_enrollments.short_description = "Ausgewählte Anmeldungen stornieren"