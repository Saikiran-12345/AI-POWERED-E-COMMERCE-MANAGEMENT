from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import SalesRecord
from .serializers import SalesRecordSerializer

class SalesRecordViewSet(viewsets.ModelViewSet):
    queryset = SalesRecord.objects.all()
    serializer_class = SalesRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

