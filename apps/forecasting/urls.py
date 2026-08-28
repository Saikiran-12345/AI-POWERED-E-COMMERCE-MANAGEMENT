from django.urls import path
from . import views
app_name = 'forecasting'
urlpatterns = [
    path('', views.ForecastDashboardView.as_view(), name='dashboard'),
]
