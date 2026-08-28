from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'report_type', 'parameters', 'generated_by', 'created_at']
    search_fields = ['name']
    list_filter = ['report_type']
    list_per_page = 50

