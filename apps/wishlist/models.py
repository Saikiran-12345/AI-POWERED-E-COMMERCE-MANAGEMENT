"""Wishlist models."""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Wishlist(models.Model):
    """User's product wishlist."""

    customer = models.OneToOneField(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('wishlist')

    def __str__(self) -> str:
        return f'Wishlist of {self.customer.user.email}'

    @property
    def item_count(self) -> int:
        return self.items.count()


class WishlistItem(models.Model):
    """Item in a wishlist."""

    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name='items'
    )
    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE, related_name='wishlist_items'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product')
        verbose_name = _('wishlist item')
        ordering = ['-added_at']

    def __str__(self) -> str:
        return f'{self.product.name} in {self.wishlist}'
