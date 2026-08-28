"""
Inventory models for stock management.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Inventory(models.Model):
    """
    Tracks stock quantities for each product.
    One-to-one relationship with Product.
    """

    product = models.OneToOneField(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='inventory'
    )
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Current available stock quantity'
    )
    reserved_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Quantity reserved for pending orders'
    )
    reorder_point = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        help_text='Quantity at which to trigger low-stock alert'
    )
    reorder_quantity = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0)],
        help_text='Suggested quantity to reorder'
    )
    warehouse_location = models.CharField(max_length=100, blank=True)
    last_restocked_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('inventory')
        verbose_name_plural = _('inventories')

    def __str__(self) -> str:
        return f'{self.product.name} — Stock: {self.quantity}'

    @property
    def available_quantity(self) -> int:
        """Quantity available for purchase (not reserved)."""
        return max(0, self.quantity - self.reserved_quantity)

    @property
    def is_low_stock(self) -> bool:
        """Check if quantity is at or below reorder point."""
        return 0 < self.quantity <= self.reorder_point

    @property
    def is_out_of_stock(self) -> bool:
        """Check if no stock available."""
        return self.available_quantity <= 0

    def reserve(self, quantity: int) -> bool:
        """
        Reserve stock for an order.
        Returns True if successful, False if insufficient stock.
        """
        if self.available_quantity >= quantity:
            self.reserved_quantity += quantity
            self.save(update_fields=['reserved_quantity', 'updated_at'])
            return True
        return False

    def release_reservation(self, quantity: int):
        """Release reserved stock (e.g., on order cancellation)."""
        self.reserved_quantity = max(0, self.reserved_quantity - quantity)
        self.save(update_fields=['reserved_quantity', 'updated_at'])

    def reduce_stock(self, quantity: int):
        """
        Reduce stock after confirmed order.
        Also releases the reservation.
        """
        self.quantity = max(0, self.quantity - quantity)
        self.reserved_quantity = max(0, self.reserved_quantity - quantity)
        self.save(update_fields=['quantity', 'reserved_quantity', 'updated_at'])

        # Update product status if out of stock
        from apps.products.signals import update_product_status_on_inventory_change
        update_product_status_on_inventory_change(self.product)

    def add_stock(self, quantity: int, note: str = ''):
        """Add stock (restocking)."""
        from django.utils import timezone
        self.quantity += quantity
        self.last_restocked_at = timezone.now()
        self.save(update_fields=['quantity', 'last_restocked_at', 'updated_at'])

        # Update product status if was out of stock
        from apps.products.signals import update_product_status_on_inventory_change
        update_product_status_on_inventory_change(self.product)

        # Log history
        InventoryHistory.objects.create(
            inventory=self,
            change_type=InventoryHistory.RESTOCK,
            quantity_changed=quantity,
            note=note
        )


class InventoryHistory(models.Model):
    """
    Tracks all inventory changes for audit purposes.
    """

    RESTOCK = 'RESTOCK'
    SALE = 'SALE'
    RESERVATION = 'RESERVATION'
    RELEASE = 'RELEASE'
    ADJUSTMENT = 'ADJUSTMENT'
    RETURN = 'RETURN'

    CHANGE_TYPE_CHOICES = [
        (RESTOCK, 'Restock'),
        (SALE, 'Sale'),
        (RESERVATION, 'Reservation'),
        (RELEASE, 'Reservation Release'),
        (ADJUSTMENT, 'Manual Adjustment'),
        (RETURN, 'Return'),
    ]

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='history'
    )
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    quantity_changed = models.IntegerField(
        help_text='Positive for additions, negative for reductions'
    )
    quantity_before = models.IntegerField(default=0)
    quantity_after = models.IntegerField(default=0)
    note = models.TextField(blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('inventory history')
        verbose_name_plural = _('inventory histories')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return (
            f'{self.inventory.product.name}: '
            f'{self.change_type} {self.quantity_changed:+d}'
        )
