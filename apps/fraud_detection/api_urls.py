from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import FraudAnalysisViewSet

router = DefaultRouter()
router.register(r'fraudanalysiss', FraudAnalysisViewSet)

app_name = 'api_fraud_detection'
urlpatterns = [
    path('', include(router.urls)),
]
