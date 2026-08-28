from django.contrib import admin
from .models import FraudAnalysis

@admin.register(FraudAnalysis)
class FraudAnalysisAdmin(admin.ModelAdmin):
    pass

