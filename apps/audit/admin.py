from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'on_delete', 'action', 'module', 'description']
    list_filter = ['object_type']
    list_per_page = 50

