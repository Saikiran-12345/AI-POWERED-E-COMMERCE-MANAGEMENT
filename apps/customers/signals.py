from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'CUSTOMER':
        from .models import Customer
        Customer.objects.get_or_create(user=instance)
