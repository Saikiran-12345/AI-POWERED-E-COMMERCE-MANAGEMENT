import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile, LoginHistory

logger = logging.getLogger(__name__)

class UserProfileService:
    """Service layer for UserProfile to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> UserProfile:
        try:
            return UserProfile.objects.get(id=obj_id)
        except UserProfile.DoesNotExist:
            logger.error(f'UserProfile with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'UserProfile not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> UserProfile:
        """Create a new UserProfile instance securely."""
        logger.info(f'Creating UserProfile with data: {kwargs}')
        instance = UserProfile(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: UserProfile, **kwargs) -> UserProfile:
        """Update an existing UserProfile instance."""
        logger.info(f'Updating UserProfile {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: UserProfile) -> bool:
        """Delete a UserProfile instance."""
        logger.warning(f'Deleting UserProfile {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active UserProfile instances if applicable."""
        if hasattr(UserProfile, 'is_active'):
            return UserProfile.objects.filter(is_active=True)
        elif hasattr(UserProfile, 'status'):
            return UserProfile.objects.filter(status='ACTIVE')
        return UserProfile.objects.all()

class LoginHistoryService:
    """Service layer for LoginHistory to abstract business logic from views and serializers."""

    @classmethod
    def get_by_id(cls, obj_id: int) -> LoginHistory:
        try:
            return LoginHistory.objects.get(id=obj_id)
        except LoginHistory.DoesNotExist:
            logger.error(f'LoginHistory with id {obj_id} not found.')
            raise ObjectDoesNotExist(f'LoginHistory not found')

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs) -> LoginHistory:
        """Create a new LoginHistory instance securely."""
        logger.info(f'Creating LoginHistory with data: {kwargs}')
        instance = LoginHistory(**kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def update(cls, instance: LoginHistory, **kwargs) -> LoginHistory:
        """Update an existing LoginHistory instance."""
        logger.info(f'Updating LoginHistory {instance.id} with data: {kwargs}')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

    @classmethod
    @transaction.atomic
    def delete(cls, instance: LoginHistory) -> bool:
        """Delete a LoginHistory instance."""
        logger.warning(f'Deleting LoginHistory {instance.id}')
        instance.delete()
        return True

    @classmethod
    def get_all_active(cls):
        """Retrieve all active LoginHistory instances if applicable."""
        if hasattr(LoginHistory, 'is_active'):
            return LoginHistory.objects.filter(is_active=True)
        elif hasattr(LoginHistory, 'status'):
            return LoginHistory.objects.filter(status='ACTIVE')
        return LoginHistory.objects.all()

