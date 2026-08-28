from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import SellerProfileViewSet

router = DefaultRouter()
router.register(r'sellerprofiles', SellerProfileViewSet)

app_name = 'api_sellers'
urlpatterns = [
    path('', include(router.urls)),
]
