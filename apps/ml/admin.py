from django.contrib import admin
from .models import MLModel
@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_type', 'version', 'is_active', 'trained_at')
    list_filter = ('model_type', 'is_active')
