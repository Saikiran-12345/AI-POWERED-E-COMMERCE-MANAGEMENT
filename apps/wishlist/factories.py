import factory
from django.utils import timezone
from faker import Faker
from .models import Wishlist, WishlistItem

fake = Faker()

class WishlistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wishlist

    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

class WishlistItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishlistItem

    added_at = factory.LazyFunction(timezone.now)

