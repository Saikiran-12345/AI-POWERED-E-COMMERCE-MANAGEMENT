from django.contrib import admin
from .models import SalesRecord
@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'product', 'quantity', 'revenue')
    list_filter = ('date',)
