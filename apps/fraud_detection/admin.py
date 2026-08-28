from django.contrib import admin
from .models import FraudAnalysis
@admin.register(FraudAnalysis)
class FraudAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'risk_level', 'anomaly_score', 'is_flagged', 'reviewed', 'created_at')
    list_filter = ('risk_level', 'is_flagged', 'reviewed')
    search_fields = ('user__email',)
