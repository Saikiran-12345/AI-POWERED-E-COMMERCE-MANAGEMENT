"""Payments models — Mock payment system."""
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
import random
import string


class PaymentMethod(models.TextChoices):
    CARD = 'CARD', _('Credit/Debit Card')
    UPI = 'UPI', _('UPI')
    NET_BANKING = 'NET_BANKING', _('Net Banking')
    CASH_ON_DELIVERY = 'CASH_ON_DELIVERY', _('Cash on Delivery')
    WALLET = 'WALLET', _('Wallet')


class PaymentStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    PROCESSING = 'PROCESSING', _('Processing')
    SUCCESS = 'SUCCESS', _('Success')
    FAILED = 'FAILED', _('Failed')
    REFUNDED = 'REFUNDED', _('Refunded')
    CANCELLED = 'CANCELLED', _('Cancelled')


class Payment(models.Model):
    """
    Mock payment record.

    ⚠️ This is a SIMULATED payment system for demonstration purposes only.
    No real financial transactions occur.
    """

    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order = models.OneToOneField(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    transaction_reference = models.CharField(max_length=100, unique=True, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    failure_reason = models.TextField(blank=True)

    # Card details (masked — never store real card data)
    card_last4 = models.CharField(max_length=4, blank=True)
    card_type = models.CharField(max_length=20, blank=True)

    # UPI
    upi_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Payment {self.transaction_reference} — {self.status}'

    def save(self, *args, **kwargs):
        if not self.transaction_reference:
            self.transaction_reference = self._generate_transaction_ref()
        super().save(*args, **kwargs)

    def _generate_transaction_ref(self) -> str:
        chars = string.ascii_uppercase + string.digits
        suffix = ''.join(random.choices(chars, k=12))
        return f'TXN-{suffix}'

    def process_mock_payment(self) -> bool:
        """
        Simulate payment processing.

        Returns True (90% success rate) for realistic demo behaviour.
        COD always succeeds.
        """
        from django.utils import timezone
        import random

        self.status = PaymentStatus.PROCESSING
        self.save(update_fields=['status'])

        # COD always succeeds
        if self.method == PaymentMethod.CASH_ON_DELIVERY:
            success = True
        else:
            # 90% success rate for other methods
            success = random.random() < 0.90

        if success:
            self.status = PaymentStatus.SUCCESS
            self.completed_at = timezone.now()
            self.gateway_response = {
                'status': 'SUCCESS',
                'message': 'Payment processed successfully (MOCK)',
                'transaction_id': self.transaction_reference,
            }
        else:
            self.status = PaymentStatus.FAILED
            self.failure_reason = 'Transaction declined (MOCK simulation)'
            self.gateway_response = {
                'status': 'FAILED',
                'message': 'Payment failed (MOCK)',
                'error_code': 'MOCK_DECLINE',
            }

        self.save(update_fields=[
            'status', 'completed_at', 'gateway_response', 'failure_reason', 'updated_at'
        ])
        return success

    @property
    def is_successful(self) -> bool:
        return self.status == PaymentStatus.SUCCESS
