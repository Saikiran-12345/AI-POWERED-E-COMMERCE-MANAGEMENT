from django.urls import path
from . import views
app_name = 'fraud_detection'
urlpatterns = [
    path('', views.FraudDashboardView.as_view(), name='dashboard'),
]
