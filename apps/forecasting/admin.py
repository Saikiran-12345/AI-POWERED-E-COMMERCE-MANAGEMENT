from django.contrib import admin
from .models import DemandForecast
@admin.register(DemandForecast)
class DemandForecastAdmin(admin.ModelAdmin):
    list_display = ('forecast_date', 'product', 'predicted_quantity', 'confidence')
    list_filter = ('forecast_date',)
