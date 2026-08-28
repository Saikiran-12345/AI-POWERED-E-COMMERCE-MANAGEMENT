from django.contrib import admin
from .models import SellerProfile

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'on_delete', 'business_name', 'business_email', 'business_phone']
    search_fields = ['business_name', 'business_email']
    list_filter = ['verification_status', 'is_active']
    list_per_page = 50

