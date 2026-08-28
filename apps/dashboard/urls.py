from django.urls import path
from . import views
app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard_redirect, name='index'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('seller/', views.seller_dashboard, name='seller'),
    path('customer/', views.customer_dashboard, name='customer'),
]
