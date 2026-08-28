from django.contrib import admin
from .models import Wishlist, WishlistItem

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'on_delete', 'created_at', 'updated_at']
    list_per_page = 50

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'wishlist', 'product', 'added_at']
    list_per_page = 50

