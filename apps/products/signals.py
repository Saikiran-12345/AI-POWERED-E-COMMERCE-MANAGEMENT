"""
Signal handlers for the products application.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


def update_product_status_on_inventory_change(product):
    """Update product status when stock goes to zero."""
    from .models import ProductStatus
    try:
        inventory = product.inventory
        if inventory.quantity <= 0:
            if product.status == ProductStatus.ACTIVE:
                product.status = ProductStatus.OUT_OF_STOCK
                product.save(update_fields=['status'])
        elif product.status == ProductStatus.OUT_OF_STOCK:
            product.status = ProductStatus.ACTIVE
            product.save(update_fields=['status'])
    except Exception:
        pass
