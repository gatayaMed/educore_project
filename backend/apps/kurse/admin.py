"""
Admin configuration for the Course model
"""

from django.contrib import admin
from .models import Kurs


@admin.register(Kurs)
class KursAdmin(admin.ModelAdmin):
    list_display = ['id', 'titel', 'start_datum', 'end_datum', 
                   'max_teilnehmer', 'verfuegbare_plaetze', 'ist_voll']
    list_filter = ['start_datum']
    search_fields = ['titel', 'beschreibung']
    readonly_fields = ['erstellt_am', 'aktualisiert_am', 'verfuegbare_plaetze']
    fieldsets = (
        ('Basisinformationen', {
            'fields': ('titel', 'beschreibung', 'max_teilnehmer')
        }),
        ('Termine', {
            'fields': ('start_datum', 'end_datum')
        }),
        ('Systeminformationen', {
            'fields': ('erstellt_am', 'aktualisiert_am', 'verfuegbare_plaetze'),
            'classes': ('collapse',)
        }),
    )