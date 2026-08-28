from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import FraudAnalysis
from .serializers import FraudAnalysisSerializer

class FraudAnalysisViewSet(viewsets.ModelViewSet):
    queryset = FraudAnalysis.objects.all()
    serializer_class = FraudAnalysisSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

