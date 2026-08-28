from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'on_delete', 'session_key', 'coupon_code', 'discount_amount']
    list_per_page = 50

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'price_at_add', 'added_at']
    list_per_page = 50

