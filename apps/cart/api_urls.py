from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cartitems', CartItemViewSet)

app_name = 'api_cart'
urlpatterns = [
    path('', include(router.urls)),
]
