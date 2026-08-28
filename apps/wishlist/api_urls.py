from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import WishlistViewSet, WishlistItemViewSet

router = DefaultRouter()
router.register(r'wishlists', WishlistViewSet)
router.register(r'wishlistitems', WishlistItemViewSet)

app_name = 'api_wishlist'
urlpatterns = [
    path('', include(router.urls)),
]
