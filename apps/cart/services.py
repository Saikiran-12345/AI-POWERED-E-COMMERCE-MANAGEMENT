import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem

logger = logging.getLogger(__name__)

class CartService:
    """Service layer for Cart to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Cart:
        try:
            return Cart.objects.get(id=obj_id)
        except Cart.DoesNotExist:
            logger.error(f'Cart with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Cart not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Cart:
        """Create a new Cart instance securely."""
        logger.info(f'Creating Cart with data: {kwargs}')
        instance = Cart(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Cart, **kwargs) -> Cart:
        """Update an existing Cart instance."""
        logger.info(f'Updating Cart {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Cart) -> bool:
        """Delete a Cart instance."""
        logger.warning(f'Deleting Cart {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Cart instances if applicable."""
        if hasattr(Cart, 'is_active'):
            return Cart.objects.filter(is_active=True)
        elif hasattr(Cart, 'status'):
            return Cart.objects.filter(status='ACTIVE')
        return Cart.objects.all()

class CartItemService:
    """Service layer for CartItem to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> CartItem:
        try:
            return CartItem.objects.get(id=obj_id)
        except CartItem.DoesNotExist:
            logger.error(f'CartItem with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'CartItem not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> CartItem:
        """Create a new CartItem instance securely."""
        logger.info(f'Creating CartItem with data: {kwargs}')
        instance = CartItem(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: CartItem, **kwargs) -> CartItem:
        """Update an existing CartItem instance."""
        logger.info(f'Updating CartItem {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: CartItem) -> bool:
        """Delete a CartItem instance."""
        logger.warning(f'Deleting CartItem {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active CartItem instances if applicable."""
        if hasattr(CartItem, 'is_active'):
            return CartItem.objects.filter(is_active=True)
        elif hasattr(CartItem, 'status'):
            return CartItem.objects.filter(status='ACTIVE')
        return CartItem.objects.all()

