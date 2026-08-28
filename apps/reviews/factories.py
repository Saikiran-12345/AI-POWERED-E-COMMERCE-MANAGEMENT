import factory
from django.utils import timezone
from faker import Faker
from .models import Review

fake = Faker()

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    rating = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    title = factory.LazyAttribute(lambda _: fake.word())
    body = factory.LazyAttribute(lambda _: fake.text())
    is_approved = factory.LazyAttribute(lambda _: fake.boolean())
    is_verified_purchase = factory.LazyAttribute(lambda _: fake.boolean())
    helpful_count = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

