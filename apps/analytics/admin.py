from django.contrib import admin
from .models import SalesRecord

@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    pass

