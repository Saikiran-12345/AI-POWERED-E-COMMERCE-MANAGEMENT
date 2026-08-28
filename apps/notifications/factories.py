import factory
from django.utils import timezone
from faker import Faker
from .models import Notification

fake = Faker()

class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    notification_type = factory.LazyAttribute(lambda _: fake.word())
    title = factory.LazyAttribute(lambda _: fake.word())
    message = factory.LazyAttribute(lambda _: fake.text())
    link = factory.LazyAttribute(lambda _: fake.word())
    is_read = factory.LazyAttribute(lambda _: fake.boolean())
    created_at = factory.LazyFunction(timezone.now)

