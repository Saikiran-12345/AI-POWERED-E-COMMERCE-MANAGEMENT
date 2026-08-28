from django.urls import path
from . import views
app_name = 'reports'
urlpatterns = [
    path('', views.reports_dashboard, name='dashboard'),
    path('sales/', views.sales_report, name='sales'),
]
