import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import DemandForecast

logger = logging.getLogger(__name__)

class DemandForecastService:
    """Service layer for DemandForecast to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> DemandForecast:
        try:
            return DemandForecast.objects.get(id=obj_id)
        except DemandForecast.DoesNotExist:
            logger.error(f'DemandForecast with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'DemandForecast not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> DemandForecast:
        """Create a new DemandForecast instance securely."""
        logger.info(f'Creating DemandForecast with data: {kwargs}')
        instance = DemandForecast(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: DemandForecast, **kwargs) -> DemandForecast:
        """Update an existing DemandForecast instance."""
        logger.info(f'Updating DemandForecast {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: DemandForecast) -> bool:
        """Delete a DemandForecast instance."""
        logger.warning(f'Deleting DemandForecast {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active DemandForecast instances if applicable."""
        if hasattr(DemandForecast, 'is_active'):
            return DemandForecast.objects.filter(is_active=True)
        elif hasattr(DemandForecast, 'status'):
            return DemandForecast.objects.filter(status='ACTIVE')
        return DemandForecast.objects.all()

