from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CustomerViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)

app_name = 'api_customers'
urlpatterns = [
    path('', include(router.urls)),
]
