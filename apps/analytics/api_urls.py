from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import SalesRecordViewSet

router = DefaultRouter()
router.register(r'salesrecords', SalesRecordViewSet)

app_name = 'api_analytics'
urlpatterns = [
    path('', include(router.urls)),
]
