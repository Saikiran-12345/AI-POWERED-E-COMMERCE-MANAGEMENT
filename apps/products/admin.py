from django.contrib import admin
from .models import Category, Product, ProductImage, ProductAttribute

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'description', 'image', 'parent']
    search_fields = ['name']
    list_filter = ['is_active']
    list_per_page = 50

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'name', 'slug', 'description', 'short_description']
    search_fields = ['name', 'meta_title']
    list_filter = ['status', 'is_featured', 'is_digital']
    list_per_page = 50

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'on_delete', 'image', 'alt_text', 'sort_order']
    list_per_page = 50

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'on_delete', 'name', 'value']
    search_fields = ['name']
    list_per_page = 50

