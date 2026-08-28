import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Report

logger = logging.getLogger(__name__)

class ReportService:
    """Service layer for Report to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Report:
        try:
            return Report.objects.get(id=obj_id)
        except Report.DoesNotExist:
            logger.error(f'Report with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Report not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Report:
        """Create a new Report instance securely."""
        logger.info(f'Creating Report with data: {kwargs}')
        instance = Report(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Report, **kwargs) -> Report:
        """Update an existing Report instance."""
        logger.info(f'Updating Report {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Report) -> bool:
        """Delete a Report instance."""
        logger.warning(f'Deleting Report {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Report instances if applicable."""
        if hasattr(Report, 'is_active'):
            return Report.objects.filter(is_active=True)
        elif hasattr(Report, 'status'):
            return Report.objects.filter(status='ACTIVE')
        return Report.objects.all()

