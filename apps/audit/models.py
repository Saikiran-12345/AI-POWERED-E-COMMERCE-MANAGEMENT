"""
Audit logging models.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class AuditLog(models.Model):
    """
    Records important system actions for audit trail.

    Tracks who did what, when, and in which module.
    """

    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('REGISTER', 'Register'),
        ('PASSWORD_CHANGE', 'Password Change'),
        ('PROFILE_UPDATE', 'Profile Update'),
        ('PRODUCT_CREATE', 'Product Created'),
        ('PRODUCT_UPDATE', 'Product Updated'),
        ('PRODUCT_DELETE', 'Product Deleted'),
        ('ORDER_CREATE', 'Order Created'),
        ('ORDER_CANCEL', 'Order Cancelled'),
        ('ORDER_STATUS_UPDATE', 'Order Status Updated'),
        ('PAYMENT_CREATE', 'Payment Created'),
        ('PAYMENT_SUCCESS', 'Payment Success'),
        ('PAYMENT_FAILED', 'Payment Failed'),
        ('INVENTORY_UPDATE', 'Inventory Updated'),
        ('REVIEW_CREATE', 'Review Created'),
        ('REVIEW_DELETE', 'Review Deleted'),
        ('USER_CREATE', 'User Created'),
        ('USER_UPDATE', 'User Updated'),
        ('USER_DELETE', 'User Deleted'),
        ('CATEGORY_CREATE', 'Category Created'),
        ('CATEGORY_UPDATE', 'Category Updated'),
        ('CATEGORY_DELETE', 'Category Deleted'),
        ('CART_ADD', 'Cart Add'),
        ('CART_REMOVE', 'Cart Remove'),
        ('WISHLIST_ADD', 'Wishlist Add'),
        ('WISHLIST_REMOVE', 'Wishlist Remove'),
        ('ML_TRAIN', 'ML Model Trained'),
        ('ML_PREDICT', 'ML Prediction Run'),
        ('REPORT_GENERATE', 'Report Generated'),
        ('ADMIN_ACTION', 'Admin Action'),
        ('SELLER_ACTION', 'Seller Action'),
        ('FRAUD_ALERT', 'Fraud Alert'),
        ('SYSTEM', 'System Event'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        db_index=True
    )
    module = models.CharField(
        max_length=100,
        db_index=True,
        help_text='Application module where the action occurred'
    )
    description = models.TextField()
    object_type = models.CharField(
        max_length=100,
        blank=True,
        help_text='The type of object affected (e.g., Product, Order)'
    )
    object_id = models.CharField(
        max_length=100,
        blank=True,
        help_text='The ID of the affected object'
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional context data as JSON'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _('audit log')
        verbose_name_plural = _('audit logs')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['module', 'timestamp']),
        ]

    def __str__(self) -> str:
        user_str = self.user.email if self.user else 'System'
        return f'[{self.timestamp.strftime("%Y-%m-%d %H:%M")}] {user_str} - {self.action}'

    @classmethod
    def get_recent(cls, days: int = 7, limit: int = 100):
        """Return recent audit logs."""
        from django.utils import timezone
        from datetime import timedelta
        since = timezone.now() - timedelta(days=days)
        return cls.objects.filter(timestamp__gte=since).select_related('user')[:limit]
