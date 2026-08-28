import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Customer

logger = logging.getLogger(__name__)

class CustomerService:
    """Service layer for Customer to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> Customer:
        try:
            return Customer.objects.get(id=obj_id)
        except Customer.DoesNotExist:
            logger.error(f'Customer with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'Customer not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> Customer:
        """Create a new Customer instance securely."""
        logger.info(f'Creating Customer with data: {kwargs}')
        instance = Customer(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: Customer, **kwargs) -> Customer:
        """Update an existing Customer instance."""
        logger.info(f'Updating Customer {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: Customer) -> bool:
        """Delete a Customer instance."""
        logger.warning(f'Deleting Customer {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active Customer instances if applicable."""
        if hasattr(Customer, 'is_active'):
            return Customer.objects.filter(is_active=True)
        elif hasattr(Customer, 'status'):
            return Customer.objects.filter(status='ACTIVE')
        return Customer.objects.all()

