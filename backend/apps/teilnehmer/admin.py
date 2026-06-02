"""
Admin configuration for the Participant model
"""

from django.contrib import admin
from .models import Teilnehmer


@admin.register(Teilnehmer)
class TeilnehmerAdmin(admin.ModelAdmin):
    list_display = ['id', 'nachname', 'vorname', 'email', 'telefon']
    list_filter = ['erstellt_am']
    search_fields = ['vorname', 'nachname', 'email']
    readonly_fields = ['erstellt_am', 'aktualisiert_am']