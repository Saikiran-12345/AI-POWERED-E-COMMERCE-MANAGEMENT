import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Order, OrderItem, OrderStatusHistory

logger = logging.getLogger(__name__)

class OrderService:
    """Service layer for Order to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Order:
        try:
            return Order.objects.get(id=obj_id)
        except Order.DoesNotExist:
            logger.error(f'Order with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Order not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Order:
        """Create a new Order instance securely."""
        logger.info(f'Creating Order with data: {kwargs}')
        instance = Order(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Order, **kwargs) -> Order:
        """Update an existing Order instance."""
        logger.info(f'Updating Order {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Order) -> bool:
        """Delete a Order instance."""
        logger.warning(f'Deleting Order {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Order instances if applicable."""
        if hasattr(Order, 'is_active'):
            return Order.objects.filter(is_active=True)
        elif hasattr(Order, 'status'):
            return Order.objects.filter(status='ACTIVE')
        return Order.objects.all()

class OrderItemService:
    """Service layer for OrderItem to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> OrderItem:
        try:
            return OrderItem.objects.get(id=obj_id)
        except OrderItem.DoesNotExist:
            logger.error(f'OrderItem with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'OrderItem not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> OrderItem:
        """Create a new OrderItem instance securely."""
        logger.info(f'Creating OrderItem with data: {kwargs}')
        instance = OrderItem(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: OrderItem, **kwargs) -> OrderItem:
        """Update an existing OrderItem instance."""
        logger.info(f'Updating OrderItem {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: OrderItem) -> bool:
        """Delete a OrderItem instance."""
        logger.warning(f'Deleting OrderItem {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active OrderItem instances if applicable."""
        if hasattr(OrderItem, 'is_active'):
            return OrderItem.objects.filter(is_active=True)
        elif hasattr(OrderItem, 'status'):
            return OrderItem.objects.filter(status='ACTIVE')
        return OrderItem.objects.all()

class OrderStatusHistoryService:
    """Service layer for OrderStatusHistory to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> OrderStatusHistory:
        try:
            return OrderStatusHistory.objects.get(id=obj_id)
        except OrderStatusHistory.DoesNotExist:
            logger.error(f'OrderStatusHistory with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'OrderStatusHistory not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> OrderStatusHistory:
        """Create a new OrderStatusHistory instance securely."""
        logger.info(f'Creating OrderStatusHistory with data: {kwargs}')
        instance = OrderStatusHistory(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: OrderStatusHistory, **kwargs) -> OrderStatusHistory:
        """Update an existing OrderStatusHistory instance."""
        logger.info(f'Updating OrderStatusHistory {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: OrderStatusHistory) -> bool:
        """Delete a OrderStatusHistory instance."""
        logger.warning(f'Deleting OrderStatusHistory {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active OrderStatusHistory instances if applicable."""
        if hasattr(OrderStatusHistory, 'is_active'):
            return OrderStatusHistory.objects.filter(is_active=True)
        elif hasattr(OrderStatusHistory, 'status'):
            return OrderStatusHistory.objects.filter(status='ACTIVE')
        return OrderStatusHistory.objects.all()

