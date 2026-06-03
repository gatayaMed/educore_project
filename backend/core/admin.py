"""
Custom admin site configuration
"""
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _


class EducoreAdminSite(AdminSite):
    """Custom admin site for Educore"""
    
    site_header = 'Educore Administration'
    site_title = 'Educore Admin Portal'
    index_title = 'Willkommen im Educore Verwaltungsportal'
    
    def get_app_list(self, request):
        """
        Customize the order of apps in admin menu
        """
        app_list = super().get_app_list(request)
        
        # Define custom order
        custom_order = ['kurse', 'teilnehmer', 'anmeldungen', 'auth', 'authtoken']
        
        # Reorder apps
        for app in app_list:
            if app['app_label'] == 'kurse':
                app['name'] = '📚 Kursverwaltung'
            elif app['app_label'] == 'teilnehmer':
                app['name'] = '👥 Teilnehmerverwaltung'
            elif app['app_label'] == 'anmeldungen':
                app['name'] = '📝 Anmeldeverwaltung'
            elif app['app_label'] == 'auth':
                app['name'] = '🔐 Benutzerverwaltung'
            elif app['app_label'] == 'authtoken':
                app['name'] = '🔑 API Tokens'
        
        return app_list


# Create custom admin site instance
admin_site = EducoreAdminSite(name='educore_admin')

# Register default models with custom site
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)