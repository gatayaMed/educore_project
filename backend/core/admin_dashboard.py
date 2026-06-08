"""
Custom admin dashboard widgets
"""
from django.contrib.admin import AdminSite
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta


class EducoreDashboard(AdminSite):
    """Dashboard with statistics"""
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        # Add custom dashboard stats
        from apps.kurse.models import Kurs
        from apps.teilnehmer.models import Teilnehmer
        from apps.anmeldungen.models import Anmeldung
        
        # Statistics
        total_courses = Kurs.objects.count()
        active_courses = Kurs.objects.filter(start_datum__gte=timezone.now().date()).count()
        total_participants = Teilnehmer.objects.count()
        total_enrollments = Anmeldung.objects.filter(status='angemeldet').count()
        
        # Recent activity
        recent_enrollments = Anmeldung.objects.filter(
            anmeldedatum__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        # Add to context
        self.extra_context = {
            'stats': {
                'total_courses': total_courses,
                'active_courses': active_courses,
                'total_participants': total_participants,
                'total_enrollments': total_enrollments,
                'recent_enrollments': recent_enrollments,
            }
        }
        
        return app_list
    
    def each_context(self, request):
        context = super().each_context(request)
        if hasattr(self, 'extra_context'):
            context.update(self.extra_context)
        return context