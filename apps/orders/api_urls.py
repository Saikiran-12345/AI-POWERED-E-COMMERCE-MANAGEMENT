from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import OrderViewSet, OrderItemViewSet, OrderStatusHistoryViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'orderitems', OrderItemViewSet)
router.register(r'orderstatushistorys', OrderStatusHistoryViewSet)

app_name = 'api_orders'
urlpatterns = [
    path('', include(router.urls)),
]
