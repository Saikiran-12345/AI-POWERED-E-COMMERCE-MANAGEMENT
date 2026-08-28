import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Payment

logger = logging.getLogger(__name__)

class PaymentService:
    """Service layer for Payment to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Payment:
        try:
            return Payment.objects.get(id=obj_id)
        except Payment.DoesNotExist:
            logger.error(f'Payment with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Payment not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Payment:
        """Create a new Payment instance securely."""
        logger.info(f'Creating Payment with data: {kwargs}')
        instance = Payment(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Payment, **kwargs) -> Payment:
        """Update an existing Payment instance."""
        logger.info(f'Updating Payment {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Payment) -> bool:
        """Delete a Payment instance."""
        logger.warning(f'Deleting Payment {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Payment instances if applicable."""
        if hasattr(Payment, 'is_active'):
            return Payment.objects.filter(is_active=True)
        elif hasattr(Payment, 'status'):
            return Payment.objects.filter(status='ACTIVE')
        return Payment.objects.all()

