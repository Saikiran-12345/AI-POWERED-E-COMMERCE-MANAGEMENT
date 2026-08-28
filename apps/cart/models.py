"""Cart models."""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    """Shopping cart - one per user, persistent across sessions."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True, blank=True
    )
    session_key = models.CharField(
        max_length=40, blank=True,
        help_text='For anonymous carts'
    )
    coupon_code = models.CharField(max_length=50, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self) -> str:
        if self.user:
            return f'Cart of {self.user.email}'
        return f'Anonymous cart ({self.session_key})'

    @property
    def total_items(self) -> int:
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def subtotal(self):
        """Sum of all item totals at discounted prices."""
        total = sum(item.total_price for item in self.items.select_related('product'))
        return round(total, 2)

    @property
    def total(self):
        """Final total after cart-level discounts."""
        return round(max(0, self.subtotal - self.discount_amount), 2)

    def clear(self):
        """Remove all items from the cart."""
        self.items.all().delete()
        self.discount_amount = 0
        self.coupon_code = ''
        self.save(update_fields=['discount_amount', 'coupon_code'])


class CartItem(models.Model):
    """Individual item in a shopping cart."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE, related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    price_at_add = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text='Price when item was added to cart'
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')

    def __str__(self) -> str:
        return f'{self.quantity}x {self.product.name}'

    @property
    def total_price(self):
        """Calculate total for this cart item."""
        return round(self.product.discounted_price * self.quantity, 2)

    @property
    def is_available(self) -> bool:
        """Check if the product is still available."""
        return (
            self.product.is_in_stock and
            self.product.stock_quantity >= self.quantity
        )
