from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import File


class FileAdmin(VersionAdmin, admin.ModelAdmin):
    fields = ('file_name', 'file_description', 'user')
    list_display = ('file_name', 'file_description', 'user')
    ordering = ['file_name', 'user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(FileAdmin, self).save_model(request, obj, form, change)


admin.site.register(File, FileAdmin)
