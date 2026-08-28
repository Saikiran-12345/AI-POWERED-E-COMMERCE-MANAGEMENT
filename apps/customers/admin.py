from django.contrib import admin
from .models import Customer
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_spent', 'order_count', 'segment', 'churn_risk')
    search_fields = ('user__email', 'user__first_name')
    list_filter = ('segment', 'churn_risk')
