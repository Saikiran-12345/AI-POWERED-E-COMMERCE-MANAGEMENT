import factory
from django.utils import timezone
from faker import Faker
from .models import Customer

fake = Faker()

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    loyalty_points = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    total_spent = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    order_count = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    segment = factory.LazyAttribute(lambda _: fake.word())
    churn_risk = factory.LazyAttribute(lambda _: fake.word())
    churn_score = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    referral_code = factory.LazyAttribute(lambda _: fake.word())
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

