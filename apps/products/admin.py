from django.contrib import admin
from .models import Category, Product, ProductImage, ProductAttribute

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    pass

