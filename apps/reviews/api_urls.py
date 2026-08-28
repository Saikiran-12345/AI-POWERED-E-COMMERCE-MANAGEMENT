from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ReviewViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

app_name = 'api_reviews'
urlpatterns = [
    path('', include(router.urls)),
]
