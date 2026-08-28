from django.contrib import admin
from .models import Inventory, InventoryHistory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'on_delete', 'quantity', 'reserved_quantity', 'reorder_point']
    list_per_page = 50

@admin.register(InventoryHistory)
class InventoryHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'inventory', 'on_delete', 'change_type', 'quantity_changed', 'quantity_before']
    list_filter = ['change_type']
    list_per_page = 50

