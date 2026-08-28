"""Notifications app models."""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """Internal notification for users."""

    TYPE_CHOICES = [
        ('ORDER_CONFIRMED', 'Order Confirmed'),
        ('ORDER_STATUS', 'Order Status Update'),
        ('ORDER_DELIVERED', 'Order Delivered'),
        ('ORDER_CANCELLED', 'Order Cancelled'),
        ('PAYMENT_SUCCESS', 'Payment Success'),
        ('PAYMENT_FAILED', 'Payment Failed'),
        ('LOW_STOCK', 'Low Stock Alert'),
        ('REVIEW_APPROVED', 'Review Approved'),
        ('RECOMMENDATION', 'New Recommendations'),
        ('SYSTEM', 'System Alert'),
        ('PROMOTION', 'Promotion'),
        ('WISHLIST', 'Wishlist Update'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.notification_type}: {self.title[:50]}'

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])

    @classmethod
    def create_notification(
        cls, user, notification_type: str, title: str, message: str, link: str = ''
    ) -> 'Notification':
        """Factory method to create a notification."""
        return cls.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link,
        )

    @classmethod
    def get_unread_count(cls, user) -> int:
        return cls.objects.filter(user=user, is_read=False).count()
