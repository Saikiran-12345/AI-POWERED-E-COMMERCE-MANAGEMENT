import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Wishlist, WishlistItem

logger = logging.getLogger(__name__)

class WishlistService:
    """Service layer for Wishlist to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Wishlist:
        try:
            return Wishlist.objects.get(id=obj_id)
        except Wishlist.DoesNotExist:
            logger.error(f'Wishlist with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Wishlist not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Wishlist:
        """Create a new Wishlist instance securely."""
        logger.info(f'Creating Wishlist with data: {kwargs}')
        instance = Wishlist(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Wishlist, **kwargs) -> Wishlist:
        """Update an existing Wishlist instance."""
        logger.info(f'Updating Wishlist {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Wishlist) -> bool:
        """Delete a Wishlist instance."""
        logger.warning(f'Deleting Wishlist {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Wishlist instances if applicable."""
        if hasattr(Wishlist, 'is_active'):
            return Wishlist.objects.filter(is_active=True)
        elif hasattr(Wishlist, 'status'):
            return Wishlist.objects.filter(status='ACTIVE')
        return Wishlist.objects.all()

class WishlistItemService:
    """Service layer for WishlistItem to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> WishlistItem:
        try:
            return WishlistItem.objects.get(id=obj_id)
        except WishlistItem.DoesNotExist:
            logger.error(f'WishlistItem with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'WishlistItem not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> WishlistItem:
        """Create a new WishlistItem instance securely."""
        logger.info(f'Creating WishlistItem with data: {kwargs}')
        instance = WishlistItem(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: WishlistItem, **kwargs) -> WishlistItem:
        """Update an existing WishlistItem instance."""
        logger.info(f'Updating WishlistItem {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: WishlistItem) -> bool:
        """Delete a WishlistItem instance."""
        logger.warning(f'Deleting WishlistItem {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active WishlistItem instances if applicable."""
        if hasattr(WishlistItem, 'is_active'):
            return WishlistItem.objects.filter(is_active=True)
        elif hasattr(WishlistItem, 'status'):
            return WishlistItem.objects.filter(status='ACTIVE')
        return WishlistItem.objects.all()

