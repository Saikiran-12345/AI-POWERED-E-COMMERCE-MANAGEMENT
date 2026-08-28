from django.urls import path
from . import views
app_name = 'ml'
urlpatterns = [
    path('', views.MLDashboardView.as_view(), name='dashboard'),
]
