from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import CoreUser


class UserAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_manager', 'is_active')
    actions = ['set_active', 'set_inactive']
    ordering = ['username', 'is_superuser', 'is_manager', 'is_active']

    def set_active(self, request, queryset):
        queryset.update(is_active=True)
    set_active.short_description = 'Mark selected user as active'

    def set_inactive(self, request, queryset):
        queryset.update(is_active=False)
    set_inactive.short_description = 'Mark selected user as inactive'


admin.site.register(CoreUser, UserAdmin)
