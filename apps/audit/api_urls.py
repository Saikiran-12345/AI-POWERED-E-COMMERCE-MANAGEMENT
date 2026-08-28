from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import AuditLogViewSet

router = DefaultRouter()
router.register(r'auditlogs', AuditLogViewSet)

app_name = 'api_audit'
urlpatterns = [
    path('', include(router.urls)),
]
