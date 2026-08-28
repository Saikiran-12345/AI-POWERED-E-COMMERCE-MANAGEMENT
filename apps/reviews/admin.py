from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'customer', 'rating', 'title', 'body']
    search_fields = ['title']
    list_filter = ['is_approved', 'is_verified_purchase']
    list_per_page = 50

