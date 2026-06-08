"""
Admin configuration for Enrollment model
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from anmeldungen.models import Anmeldung


@admin.register(Anmeldung)
class AnmeldungAdmin(admin.ModelAdmin):
    list_display = ['id', 'kurs_link', 'teilnehmer_link', 'anmeldedatum', 
                   'status_badge', 'ist_aktiv']
    
    list_filter = ['status', 'anmeldedatum', 'kurs']
    
    search_fields = ['kurs__titel', 'teilnehmer__vorname', 'teilnehmer__nachname', 'teilnehmer__email']
    
    readonly_fields = ['anmeldedatum']
    
    fieldsets = (
        ('Anmeldeinformationen', {
            'fields': ('kurs', 'teilnehmer', 'status'),
            'classes': ('wide',)
        }),
        ('Zeitinformationen', {
            'fields': ('anmeldedatum',),
            'classes': ('wide',)
        }),
    )
    
    actions = ['cancel_selected_enrollments', 'activate_selected_enrollments', 'export_as_csv']
    
    list_per_page = 25
    ordering = ['-anmeldedatum']
    date_hierarchy = 'anmeldedatum'
    
    def kurs_link(self, obj):
        """Link to course admin"""
        url = reverse('admin:kurse_kurs_change', args=[obj.kurs.id])
        return format_html('<a href="{}">{}</a>', url, obj.kurs.titel)
    kurs_link.short_description = 'Kurs'
    
    def teilnehmer_link(self, obj):
        """Link to participant admin"""
        url = reverse('admin:teilnehmer_teilnehmer_change', args=[obj.teilnehmer.id])
        return format_html('<a href="{}">{}</a>', url, obj.teilnehmer.vollstaendiger_name)
    teilnehmer_link.short_description = 'Teilnehmer'
    
    def status_badge(self, obj):
        """Display colored status badge"""
        if obj.status == 'angemeldet':
            return format_html('<span style="background-color: #28a745; padding: 3px 8px; border-radius: 3px; color: white;">✅ Angemeldet</span>')
        else:
            return format_html('<span style="background-color: #dc3545; padding: 3px 8px; border-radius: 3px; color: white;">❌ Storniert</span>')
    status_badge.short_description = 'Status'
    
    def ist_aktiv(self, obj):
        """Check if enrollment is active"""
        return obj.status == 'angemeldet'
    ist_aktiv.boolean = True
    ist_aktiv.short_description = 'Aktiv'
    
    def cancel_selected_enrollments(self, request, queryset):
        """Cancel selected enrollments"""
        count = 0
        for enrollment in queryset:
            if enrollment.status == 'angemeldet':
                enrollment.cancel()
                count += 1
        self.message_user(request, f"{count} Anmeldung(en) wurden storniert.")
    
    cancel_selected_enrollments.short_description = "Ausgewählte Anmeldungen stornieren"
    
    def activate_selected_enrollments(self, request, queryset):
        """Activate selected enrollments"""
        count = queryset.filter(status='storniert').update(status='angemeldet')
        self.message_user(request, f"{count} Anmeldung(en) wurden reaktiviert.")
    
    activate_selected_enrollments.short_description = "Ausgewählte Anmeldungen reaktivieren"
    
    def export_as_csv(self, request, queryset):
        """Export enrollments as CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="anmeldungen_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Kurs', 'Teilnehmer', 'Email', 'Anmeldedatum', 'Status'])
        
        for enrollment in queryset:
            writer.writerow([
                enrollment.id, 
                enrollment.kurs.titel,
                enrollment.teilnehmer.vollstaendiger_name,
                enrollment.teilnehmer.email,
                enrollment.anmeldedatum.strftime('%Y-%m-%d %H:%M'),
                enrollment.get_status_display()
            ])
        
        return response
    
    export_as_csv.short_description = "Als CSV exportieren"