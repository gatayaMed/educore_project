"""
Custom admin site configuration
"""
from django.contrib.admin import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _



admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)