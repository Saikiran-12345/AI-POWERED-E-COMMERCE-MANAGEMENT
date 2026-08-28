from django.contrib import admin
from .models import SalesRecord

@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'product', 'category', 'seller', 'quantity']
    list_per_page = 50

