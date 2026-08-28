from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import DemandForecastViewSet

router = DefaultRouter()
router.register(r'demandforecasts', DemandForecastViewSet)

app_name = 'api_forecasting'
urlpatterns = [
    path('', include(router.urls)),
]
