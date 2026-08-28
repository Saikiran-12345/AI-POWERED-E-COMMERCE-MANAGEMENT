from django.contrib import admin
from .models import Inventory, InventoryHistory
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'reserved_quantity', 'is_low_stock')
    search_fields = ('product__name',)
    list_filter = ('updated_at',)
@admin.register(InventoryHistory)
class InventoryHistoryAdmin(admin.ModelAdmin):
    list_display = ('inventory', 'change_type', 'quantity_changed', 'created_at')
    list_filter = ('change_type',)
    readonly_fields = ('inventory', 'quantity_before', 'quantity_after', 'created_at')
