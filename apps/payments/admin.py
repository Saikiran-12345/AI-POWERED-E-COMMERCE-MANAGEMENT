from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_id', 'order', 'on_delete', 'amount', 'method']
    list_filter = ['status', 'card_type']
    list_per_page = 50

