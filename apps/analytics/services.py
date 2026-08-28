import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import SalesRecord

logger = logging.getLogger(__name__)

class SalesRecordService:
    """Service layer for SalesRecord to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> SalesRecord:
        try:
            return SalesRecord.objects.get(id=obj_id)
        except SalesRecord.DoesNotExist:
            logger.error(f'SalesRecord with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'SalesRecord not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> SalesRecord:
        """Create a new SalesRecord instance securely."""
        logger.info(f'Creating SalesRecord with data: {kwargs}')
        instance = SalesRecord(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: SalesRecord, **kwargs) -> SalesRecord:
        """Update an existing SalesRecord instance."""
        logger.info(f'Updating SalesRecord {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: SalesRecord) -> bool:
        """Delete a SalesRecord instance."""
        logger.warning(f'Deleting SalesRecord {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active SalesRecord instances if applicable."""
        if hasattr(SalesRecord, 'is_active'):
            return SalesRecord.objects.filter(is_active=True)
        elif hasattr(SalesRecord, 'status'):
            return SalesRecord.objects.filter(status='ACTIVE')
        return SalesRecord.objects.all()

