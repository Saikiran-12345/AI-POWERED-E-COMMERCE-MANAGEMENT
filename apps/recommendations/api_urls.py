from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import RecommendationViewSet

router = DefaultRouter()
router.register(r'recommendations', RecommendationViewSet)

app_name = 'api_recommendations'
urlpatterns = [
    path('', include(router.urls)),
]
