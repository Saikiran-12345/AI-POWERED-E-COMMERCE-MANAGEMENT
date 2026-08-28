from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_number', 'customer', 'on_delete', 'status', 'subtotal']
    search_fields = ['shipping_name', 'shipping_email']
    list_filter = ['status']
    list_per_page = 50

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'product_name', 'product_sku', 'quantity']
    search_fields = ['product_name']
    list_per_page = 50

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'old_status', 'new_status', 'note', 'changed_by']
    list_filter = ['old_status', 'new_status']
    list_per_page = 50

