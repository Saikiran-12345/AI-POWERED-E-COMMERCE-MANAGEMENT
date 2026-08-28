import factory
from django.utils import timezone
from faker import Faker
from .models import Payment

fake = Faker()

class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    amount = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    method = factory.LazyAttribute(lambda _: fake.word())
    status = factory.LazyAttribute(lambda _: fake.word())
    transaction_reference = factory.LazyAttribute(lambda _: fake.word())
    failure_reason = factory.LazyAttribute(lambda _: fake.text())
    card_type = factory.LazyAttribute(lambda _: fake.word())
    upi_id = factory.LazyAttribute(lambda _: fake.word())
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    completed_at = factory.LazyFunction(timezone.now)

