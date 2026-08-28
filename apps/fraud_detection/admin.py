from django.contrib import admin
from .models import FraudAnalysis

@admin.register(FraudAnalysis)
class FraudAnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'user', 'anomaly_score', 'risk_level', 'flags']
    list_filter = ['is_flagged']
    list_per_page = 50

