"""Wishlist URL patterns."""
from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('add/<int:product_id>/', views.add_to_wishlist, name='add'),
    path('remove/<int:item_id>/', views.remove_from_wishlist, name='remove'),
    path('move-to-cart/<int:item_id>/', views.move_to_cart, name='move_to_cart'),
]
