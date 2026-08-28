"""Sellers app models."""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class SellerProfile(models.Model):
    """Extended seller profile with business information."""

    VERIFICATION_STATUS = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
        ('SUSPENDED', 'Suspended'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seller_profile'
    )
    business_name = models.CharField(max_length=255)
    business_email = models.EmailField(blank=True)
    business_phone = models.CharField(max_length=20, blank=True)
    business_address = models.TextField(blank=True)
    gst_number = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    bank_account = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=11, blank=True)
    verification_status = models.CharField(
        max_length=20, choices=VERIFICATION_STATUS, default='PENDING'
    )
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_orders = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    bio = models.TextField(blank=True)
    logo = models.ImageField(upload_to='sellers/logos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('seller profile')
        verbose_name_plural = _('seller profiles')

    def __str__(self) -> str:
        return f'Seller: {self.business_name}'

    @property
    def product_count(self) -> int:
        return self.user.products.count()

    def update_sales_stats(self):
        """Recalculate sales statistics."""
        from apps.orders.models import OrderItem, OrderStatus
        delivered_items = OrderItem.objects.filter(
            seller=self.user,
            order__status=OrderStatus.DELIVERED
        )
        from django.db.models import Sum, Count
        stats = delivered_items.aggregate(
            total_sales=Sum('total_price'),
            total_orders=Count('order', distinct=True)
        )
        self.total_sales = stats['total_sales'] or 0
        self.total_orders = stats['total_orders'] or 0
        self.save(update_fields=['total_sales', 'total_orders', 'updated_at'])
