import factory
from django.utils import timezone
from faker import Faker
from .models import AuditLog

fake = Faker()

class AuditLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AuditLog

    action = factory.LazyAttribute(lambda _: fake.word())
    module = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())
    object_type = factory.LazyAttribute(lambda _: fake.word())
    object_id = factory.LazyAttribute(lambda _: fake.word())
    user_agent = factory.LazyAttribute(lambda _: fake.word())
    timestamp = factory.LazyFunction(timezone.now)

