from django.urls import path
from . import views
app_name = 'payments'
urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('process/', views.process_payment, name='process'),
]
