from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import InventoryViewSet, InventoryHistoryViewSet

router = DefaultRouter()
router.register(r'inventorys', InventoryViewSet)
router.register(r'inventoryhistorys', InventoryHistoryViewSet)

app_name = 'api_inventory'
urlpatterns = [
    path('', include(router.urls)),
]
