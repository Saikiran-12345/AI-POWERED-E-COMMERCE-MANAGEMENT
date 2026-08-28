from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ReportViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet)

app_name = 'api_reports'
urlpatterns = [
    path('', include(router.urls)),
]
