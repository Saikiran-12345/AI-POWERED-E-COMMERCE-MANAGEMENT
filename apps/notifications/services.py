import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Notification

logger = logging.getLogger(__name__)

class NotificationService:
    """Service layer for Notification to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Notification:
        try:
            return Notification.objects.get(id=obj_id)
        except Notification.DoesNotExist:
            logger.error(f'Notification with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Notification not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Notification:
        """Create a new Notification instance securely."""
        logger.info(f'Creating Notification with data: {kwargs}')
        instance = Notification(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Notification, **kwargs) -> Notification:
        """Update an existing Notification instance."""
        logger.info(f'Updating Notification {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Notification) -> bool:
        """Delete a Notification instance."""
        logger.warning(f'Deleting Notification {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Notification instances if applicable."""
        if hasattr(Notification, 'is_active'):
            return Notification.objects.filter(is_active=True)
        elif hasattr(Notification, 'status'):
            return Notification.objects.filter(status='ACTIVE')
        return Notification.objects.all()

