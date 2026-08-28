import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Review

logger = logging.getLogger(__name__)

class ReviewService:
    """Service layer for Review to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Review:
        try:
            return Review.objects.get(id=obj_id)
        except Review.DoesNotExist:
            logger.error(f'Review with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Review not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Review:
        """Create a new Review instance securely."""
        logger.info(f'Creating Review with data: {kwargs}')
        instance = Review(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Review, **kwargs) -> Review:
        """Update an existing Review instance."""
        logger.info(f'Updating Review {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Review) -> bool:
        """Delete a Review instance."""
        logger.warning(f'Deleting Review {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Review instances if applicable."""
        if hasattr(Review, 'is_active'):
            return Review.objects.filter(is_active=True)
        elif hasattr(Review, 'status'):
            return Review.objects.filter(status='ACTIVE')
        return Review.objects.all()

