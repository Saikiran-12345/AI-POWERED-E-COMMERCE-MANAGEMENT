from django.contrib import admin
from .models import DemandForecast

@admin.register(DemandForecast)
class DemandForecastAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'category', 'forecast_date', 'predicted_quantity', 'confidence']
    list_per_page = 50

