"""Customers app models."""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    """Extended customer profile linked to User."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    loyalty_points = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    order_count = models.PositiveIntegerField(default=0)
    segment = models.CharField(max_length=50, blank=True, help_text='ML-assigned segment')
    churn_risk = models.CharField(
        max_length=20, blank=True,
        choices=[
            ('LOW', 'Low Risk'),
            ('MEDIUM', 'Medium Risk'),
            ('HIGH', 'High Risk'),
        ]
    )
    churn_score = models.FloatField(default=0.0)
    referral_code = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')

    def __str__(self) -> str:
        return f'Customer: {self.user.get_full_name()}'

    def save(self, *args, **kwargs):
        if not self.referral_code:
            import random, string
            self.referral_code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
        super().save(*args, **kwargs)

    @property
    def average_order_value(self):
        if self.order_count > 0:
            return round(self.total_spent / self.order_count, 2)
        return 0

    def update_stats(self):
        """Recalculate order stats from actual order data."""
        from apps.orders.models import OrderStatus
        completed_orders = self.orders.filter(
            status__in=[OrderStatus.DELIVERED, OrderStatus.SHIPPED]
        )
        self.order_count = completed_orders.count()
        self.total_spent = completed_orders.aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0
        self.save(update_fields=['order_count', 'total_spent', 'updated_at'])
