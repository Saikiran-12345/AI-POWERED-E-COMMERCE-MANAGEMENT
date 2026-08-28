from django.urls import path
from . import views
app_name = 'sellers'
urlpatterns = [
    path('', views.SellerListView.as_view(), name='list'),
]
