"""Reviews app models."""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    """Product review and rating by a customer."""

    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE, related_name='reviews'
    )
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5'
    )
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    is_approved = models.BooleanField(default=True)
    is_verified_purchase = models.BooleanField(
        default=False,
        help_text='True if customer actually purchased this product'
    )
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        unique_together = ('product', 'customer')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.customer.user.get_short_name()} rated {self.product.name}: {self.rating}/5'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update product's denormalized rating
        self.product.update_rating()

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        product.update_rating()
