from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'on_delete', 'notification_type', 'title', 'message']
    search_fields = ['title']
    list_filter = ['notification_type', 'is_read']
    list_per_page = 50

