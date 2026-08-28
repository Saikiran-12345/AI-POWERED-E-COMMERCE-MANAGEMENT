import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import SellerProfile

logger = logging.getLogger(__name__)

class SellerProfileService:
    """Service layer for SellerProfile to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> SellerProfile:
        try:
            return SellerProfile.objects.get(id=obj_id)
        except SellerProfile.DoesNotExist:
            logger.error(f'SellerProfile with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'SellerProfile not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> SellerProfile:
        """Create a new SellerProfile instance securely."""
        logger.info(f'Creating SellerProfile with data: {kwargs}')
        instance = SellerProfile(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: SellerProfile, **kwargs) -> SellerProfile:
        """Update an existing SellerProfile instance."""
        logger.info(f'Updating SellerProfile {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: SellerProfile) -> bool:
        """Delete a SellerProfile instance."""
        logger.warning(f'Deleting SellerProfile {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active SellerProfile instances if applicable."""
        if hasattr(SellerProfile, 'is_active'):
            return SellerProfile.objects.filter(is_active=True)
        elif hasattr(SellerProfile, 'status'):
            return SellerProfile.objects.filter(status='ACTIVE')
        return SellerProfile.objects.all()

