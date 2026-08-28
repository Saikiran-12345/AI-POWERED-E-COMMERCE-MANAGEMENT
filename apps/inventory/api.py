from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Inventory, InventoryHistory
from .serializers import InventorySerializer, InventoryHistorySerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

class InventoryHistoryViewSet(viewsets.ModelViewSet):
    queryset = InventoryHistory.objects.all()
    serializer_class = InventoryHistorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

