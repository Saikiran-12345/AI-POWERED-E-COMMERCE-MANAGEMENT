"""
Admin configuration for audit logs.
"""

from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin for AuditLog model — read-only."""

    list_display = ('timestamp', 'user', 'action', 'module', 'description')
    list_filter = ('action', 'module', 'timestamp')
    search_fields = ('user__email', 'description', 'object_type', 'object_id')
    readonly_fields = (
        'user', 'action', 'module', 'description',
        'object_type', 'object_id', 'extra_data',
        'ip_address', 'user_agent', 'timestamp'
    )
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
