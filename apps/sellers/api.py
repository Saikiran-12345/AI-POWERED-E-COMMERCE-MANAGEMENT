from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import SellerProfile
from .serializers import SellerProfileSerializer

class SellerProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

