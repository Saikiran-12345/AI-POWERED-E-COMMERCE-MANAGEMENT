import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Recommendation

logger = logging.getLogger(__name__)

class RecommendationService:
    """Service layer for Recommendation to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Recommendation:
        try:
            return Recommendation.objects.get(id=obj_id)
        except Recommendation.DoesNotExist:
            logger.error(f'Recommendation with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Recommendation not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Recommendation:
        """Create a new Recommendation instance securely."""
        logger.info(f'Creating Recommendation with data: {kwargs}')
        instance = Recommendation(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Recommendation, **kwargs) -> Recommendation:
        """Update an existing Recommendation instance."""
        logger.info(f'Updating Recommendation {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Recommendation) -> bool:
        """Delete a Recommendation instance."""
        logger.warning(f'Deleting Recommendation {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Recommendation instances if applicable."""
        if hasattr(Recommendation, 'is_active'):
            return Recommendation.objects.filter(is_active=True)
        elif hasattr(Recommendation, 'status'):
            return Recommendation.objects.filter(status='ACTIVE')
        return Recommendation.objects.all()

