from django.contrib import admin
from .models import Wishlist, WishlistItem

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    pass

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    pass

