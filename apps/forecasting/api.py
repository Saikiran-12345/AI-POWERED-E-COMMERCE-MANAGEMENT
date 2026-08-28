from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import DemandForecast
from .serializers import DemandForecastSerializer

class DemandForecastViewSet(viewsets.ModelViewSet):
    queryset = DemandForecast.objects.all()
    serializer_class = DemandForecastSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

