import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Inventory, InventoryHistory

logger = logging.getLogger(__name__)

class InventoryService:
    """Service layer for Inventory to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Inventory:
        try:
            return Inventory.objects.get(id=obj_id)
        except Inventory.DoesNotExist:
            logger.error(f'Inventory with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Inventory not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Inventory:
        """Create a new Inventory instance securely."""
        logger.info(f'Creating Inventory with data: {kwargs}')
        instance = Inventory(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Inventory, **kwargs) -> Inventory:
        """Update an existing Inventory instance."""
        logger.info(f'Updating Inventory {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Inventory) -> bool:
        """Delete a Inventory instance."""
        logger.warning(f'Deleting Inventory {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Inventory instances if applicable."""
        if hasattr(Inventory, 'is_active'):
            return Inventory.objects.filter(is_active=True)
        elif hasattr(Inventory, 'status'):
            return Inventory.objects.filter(status='ACTIVE')
        return Inventory.objects.all()

class InventoryHistoryService:
    """Service layer for InventoryHistory to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> InventoryHistory:
        try:
            return InventoryHistory.objects.get(id=obj_id)
        except InventoryHistory.DoesNotExist:
            logger.error(f'InventoryHistory with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'InventoryHistory not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> InventoryHistory:
        """Create a new InventoryHistory instance securely."""
        logger.info(f'Creating InventoryHistory with data: {kwargs}')
        instance = InventoryHistory(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: InventoryHistory, **kwargs) -> InventoryHistory:
        """Update an existing InventoryHistory instance."""
        logger.info(f'Updating InventoryHistory {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: InventoryHistory) -> bool:
        """Delete a InventoryHistory instance."""
        logger.warning(f'Deleting InventoryHistory {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active InventoryHistory instances if applicable."""
        if hasattr(InventoryHistory, 'is_active'):
            return InventoryHistory.objects.filter(is_active=True)
        elif hasattr(InventoryHistory, 'status'):
            return InventoryHistory.objects.filter(status='ACTIVE')
        return InventoryHistory.objects.all()

