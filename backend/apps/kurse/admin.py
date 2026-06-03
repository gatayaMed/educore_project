"""
Enhanced Admin configuration for Course model
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Kurs


@admin.register(Kurs)
class KursAdmin(admin.ModelAdmin):
    # List display - show important fields
    list_display = ['id', 'titel', 'start_datum', 'end_datum', 
                   'max_teilnehmer', 'verfuegbare_plaetze', 
                   'ist_voll_badge', 'auslastung_balken']
    
    # Filters for sidebar
    list_filter = ['start_datum', 'end_datum', 'aktualisiert_am']
    
    # Search fields
    search_fields = ['titel', 'beschreibung']
    
    # Date hierarchy for navigation
    date_hierarchy = 'start_datum'
    
    # Read-only fields
    readonly_fields = ['erstellt_am', 'aktualisiert_am', 
                      'verfuegbare_plaetze', 'anzahl_anmeldungen',
                      'auslastung_prozent']
    
    # Fieldsets for organizing form layout
    fieldsets = (
        ('Basisinformationen', {
            'fields': ('titel', 'beschreibung'),
            'classes': ('wide',)
        }),
        ('Termine & Kapazität', {
            'fields': ('start_datum', 'end_datum', 'max_teilnehmer'),
            'classes': ('wide',)
        }),
        ('Statistiken', {
            'fields': ('verfuegbare_plaetze', 'anzahl_anmeldungen', 'auslastung_prozent'),
            'classes': ('collapse', 'wide')
        }),
        ('Systeminformationen', {
            'fields': ('erstellt_am', 'aktualisiert_am'),
            'classes': ('collapse',)
        }),
    )
    
    # Actions for bulk operations
    actions = ['duplicate_courses', 'export_as_csv']
    
    # List editable fields (inline editing)
    list_editable = ['max_teilnehmer']
    
    # Number of items per page
    list_per_page = 25
    
    # Default ordering
    ordering = ['-start_datum']
    
    def ist_voll_badge(self, obj):
        """Display colored badge for course status"""
        if obj.ist_voll:
            return format_html('<span style="background-color: #dc3545; padding: 5px 10px; border-radius: 3px; color: white;">🔴 Ausgebucht</span>')
        elif obj.verfuegbare_plaetze < 5:
            return format_html('<span style="background-color: #ffc107; padding: 5px 10px; border-radius: 3px; color: black;">🟡 Wenige Plätze ({})</span>', obj.verfuegbare_plaetze)
        else:
            return format_html('<span style="background-color: #28a745; padding: 5px 10px; border-radius: 3px; color: white;">🟢 Plätze frei ({})</span>', obj.verfuegbare_plaetze)
    
    ist_voll_badge.short_description = 'Status'
    
    def auslastung_balken(self, obj):
        """Display progress bar for course utilization"""
        if obj.max_teilnehmer > 0:
            prozent = (obj.anzahl_anmeldungen / obj.max_teilnehmer) * 100
            color = 'red' if prozent > 90 else 'orange' if prozent > 70 else 'green'
            return format_html(
                '<div style="width: 100px; background-color: #e9ecef; border-radius: 10px; overflow: hidden;">'
                '<div style="width: {}%; background-color: {}; text-align: center; color: white; font-size: 11px;">{:.0f}%</div></div>',
                prozent, color, prozent
            )
        return format_html('<span style="color: gray;">-</span>')
    
    auslastung_balken.short_description = 'Auslastung'
    
    def auslastung_prozent(self, obj):
        """Calculate utilization percentage"""
        if obj.max_teilnehmer > 0:
            return f"{(obj.anzahl_anmeldungen / obj.max_teilnehmer) * 100:.1f}%"
        return "0%"
    auslastung_prozent.short_description = 'Auslastung %'
    
    def duplicate_courses(self, request, queryset):
        """Duplicate selected courses"""
        for course in queryset:
            course.pk = None
            course.titel = f"{course.titel} (Kopie)"
            course.save()
        self.message_user(request, f"{queryset.count()} Kurs(e) wurden dupliziert.")
    
    duplicate_courses.short_description = "Ausgewählte Kurse duplizieren"
    
    def export_as_csv(self, request, queryset):
        """Export selected courses as CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="kurse_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Titel', 'Startdatum', 'Enddatum', 'Max Teilnehmer', 'Aktive Anmeldungen', 'Verfügbare Plätze'])
        
        for course in queryset:
            writer.writerow([
                course.id, course.titel, course.start_datum, 
                course.end_datum, course.max_teilnehmer,
                course.anzahl_anmeldungen, course.verfuegbare_plaetze
            ])
        
        return response
    
    export_as_csv.short_description = "Als CSV exportieren"