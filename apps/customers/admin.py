from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'on_delete', 'loyalty_points', 'total_spent', 'order_count']
    list_per_page = 50

