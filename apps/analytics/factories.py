import factory
from django.utils import timezone
from faker import Faker
from .models import SalesRecord

fake = Faker()

class SalesRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SalesRecord

    date = factory.LazyFunction(timezone.now)
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    revenue = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    created_at = factory.LazyFunction(timezone.now)

