from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_seller_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'SELLER':
        from .models import SellerProfile
        SellerProfile.objects.get_or_create(user=instance, defaults={'business_name': instance.get_full_name() or instance.email})
