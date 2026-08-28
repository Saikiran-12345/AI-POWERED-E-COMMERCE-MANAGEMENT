import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import AuditLog

logger = logging.getLogger(__name__)

class AuditLogService:
    """Service layer for AuditLog to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> AuditLog:
        try:
            return AuditLog.objects.get(id=obj_id)
        except AuditLog.DoesNotExist:
            logger.error(f'AuditLog with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'AuditLog not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> AuditLog:
        """Create a new AuditLog instance securely."""
        logger.info(f'Creating AuditLog with data: {kwargs}')
        instance = AuditLog(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: AuditLog, **kwargs) -> AuditLog:
        """Update an existing AuditLog instance."""
        logger.info(f'Updating AuditLog {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: AuditLog) -> bool:
        """Delete a AuditLog instance."""
        logger.warning(f'Deleting AuditLog {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active AuditLog instances if applicable."""
        if hasattr(AuditLog, 'is_active'):
            return AuditLog.objects.filter(is_active=True)
        elif hasattr(AuditLog, 'status'):
            return AuditLog.objects.filter(status='ACTIVE')
        return AuditLog.objects.all()

