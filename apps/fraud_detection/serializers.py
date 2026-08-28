from rest_framework import serializers
from .models import FraudAnalysis

class FraudAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudAnalysis
        fields = '__all__'

