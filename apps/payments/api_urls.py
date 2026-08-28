from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

app_name = 'api_payments'
urlpatterns = [
    path('', include(router.urls)),
]
