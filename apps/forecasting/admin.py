from django.contrib import admin
from .models import DemandForecast

@admin.register(DemandForecast)
class DemandForecastAdmin(admin.ModelAdmin):
    pass

