from django.contrib import admin
from .models import SellerProfile
@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'verification_status', 'total_sales')
    list_filter = ('verification_status', 'is_active')
    search_fields = ('business_name', 'user__email')
