import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import FraudAnalysis

logger = logging.getLogger(__name__)

class FraudAnalysisService:
    """Service layer for FraudAnalysis to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> FraudAnalysis:
        try:
            return FraudAnalysis.objects.get(id=obj_id)
        except FraudAnalysis.DoesNotExist:
            logger.error(f'FraudAnalysis with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'FraudAnalysis not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> FraudAnalysis:
        """Create a new FraudAnalysis instance securely."""
        logger.info(f'Creating FraudAnalysis with data: {kwargs}')
        instance = FraudAnalysis(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: FraudAnalysis, **kwargs) -> FraudAnalysis:
        """Update an existing FraudAnalysis instance."""
        logger.info(f'Updating FraudAnalysis {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: FraudAnalysis) -> bool:
        """Delete a FraudAnalysis instance."""
        logger.warning(f'Deleting FraudAnalysis {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active FraudAnalysis instances if applicable."""
        if hasattr(FraudAnalysis, 'is_active'):
            return FraudAnalysis.objects.filter(is_active=True)
        elif hasattr(FraudAnalysis, 'status'):
            return FraudAnalysis.objects.filter(status='ACTIVE')
        return FraudAnalysis.objects.all()

