"""
Enhanced Admin configuration for Participant model
"""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import Count
from .models import Teilnehmer


@admin.register(Teilnehmer)
class TeilnehmerAdmin(admin.ModelAdmin):
    list_display = ['id', 'vollstaendiger_name_link', 'email', 'telefon', 
                   'anzahl_anmeldungen', 'aktive_anmeldungen', 'erstellt_am']
    
    list_filter = ['erstellt_am', 'aktualisiert_am']
    
    search_fields = ['vorname', 'nachname', 'email', 'telefon']
    
    readonly_fields = ['erstellt_am', 'aktualisiert_am', 'anzahl_anmeldungen', 
                      'aktive_anmeldungen', 'anmeldungen_details']
    
    fieldsets = (
        ('Persönliche Informationen', {
            'fields': ('vorname', 'nachname', 'email', 'telefon'),
            'classes': ('wide',)
        }),
        ('Teilnehmerstatistiken', {
            'fields': ('anzahl_anmeldungen', 'aktive_anmeldungen', 'anmeldungen_details'),
            'classes': ('collapse',)
        }),
        ('Systeminformationen', {
            'fields': ('erstellt_am', 'aktualisiert_am'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['send_email_to_selected', 'export_as_csv']
    
    list_per_page = 25
    ordering = ['-erstellt_am']
    
    def vollstaendiger_name_link(self, obj):
        """Display name as link to detail page"""
        url = reverse('admin:teilnehmer_teilnehmer_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.vollstaendiger_name)
    
    vollstaendiger_name_link.short_description = 'Name'
    
    def anzahl_anmeldungen(self, obj):
        """Total number of enrollments (including cancelled)"""
        return obj.anmeldungen.count()
    anzahl_anmeldungen.short_description = 'Gesamt Anmeldungen'
    
    def aktive_anmeldungen(self, obj):
        """Number of active enrollments"""
        count = obj.anmeldungen.filter(status='angemeldet').count()
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', count)
    aktive_anmeldungen.short_description = 'Aktive Anmeldungen'
    
    def anmeldungen_details(self, obj):
        """Display detailed list of enrollments"""
        enrollments = obj.anmeldungen.all().select_related('kurs')[:10]
        if not enrollments:
            return "Keine Anmeldungen"
        
        html = '<ul style="margin: 0; padding-left: 20px;">'
        for enrollment in enrollments:
            status_color = 'green' if enrollment.status == 'angemeldet' else 'red'
            html += f'<li><a href="{reverse("admin:anmeldungen_anmeldung_change", args=[enrollment.id])}">{enrollment.kurs.titel}</a> - '
            html += f'<span style="color: {status_color};">{enrollment.get_status_display()}</span>'
            html += f' <small>({enrollment.anmeldedatum|date:"d.m.Y"})</small></li>'
        html += '</ul>'
        
        if obj.anmeldungen.count() > 10:
            html += f'<small>... und {obj.anmeldungen.count() - 10} weitere</small>'
        
        return format_html(html)
    anmeldungen_details.short_description = 'Kursanmeldungen'
    
    def send_email_to_selected(self, request, queryset):
        """Send email to selected participants"""
        # Implement email sending logic here
        self.message_user(request, f"Email würde an {queryset.count()} Teilnehmer gesendet werden.")
    
    send_email_to_selected.short_description = "E-Mail an ausgewählte Teilnehmer"
    
    def export_as_csv(self, request, queryset):
        """Export participants as CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="teilnehmer_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Vorname', 'Nachname', 'Email', 'Telefon', 'Anmeldungen', 'Erstellt am'])
        
        for participant in queryset:
            writer.writerow([
                participant.id, participant.vorname, participant.nachname,
                participant.email, participant.telefon, 
                participant.anmeldungen.count(),
                participant.erstellt_am.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
    
    export_as_csv.short_description = "Als CSV exportieren"