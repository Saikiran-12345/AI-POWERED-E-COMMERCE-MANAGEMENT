from django.contrib import admin
from .models import Inventory, InventoryHistory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    pass

@admin.register(InventoryHistory)
class InventoryHistoryAdmin(admin.ModelAdmin):
    pass

