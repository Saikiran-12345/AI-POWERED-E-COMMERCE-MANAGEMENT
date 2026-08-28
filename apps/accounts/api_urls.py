from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import UserProfileViewSet, LoginHistoryViewSet

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'loginhistorys', LoginHistoryViewSet)

app_name = 'api_accounts'
urlpatterns = [
    path('', include(router.urls)),
]
