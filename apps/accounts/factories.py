import factory
from django.utils import timezone
from faker import Faker
from .models import UserProfile, LoginHistory

fake = Faker()

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    bio = factory.LazyAttribute(lambda _: fake.text())
    date_of_birth = factory.LazyFunction(timezone.now)
    gender = factory.LazyAttribute(lambda _: fake.word())
    city = factory.LazyAttribute(lambda _: fake.word())
    state = factory.LazyAttribute(lambda _: fake.word())
    pincode = factory.LazyAttribute(lambda _: fake.word())
    country = factory.LazyAttribute(lambda _: fake.word())
    newsletter_subscribed = factory.LazyAttribute(lambda _: fake.boolean())
    email_notifications = factory.LazyAttribute(lambda _: fake.boolean())
    sms_notifications = factory.LazyAttribute(lambda _: fake.boolean())
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

class LoginHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LoginHistory

    login_time = factory.LazyFunction(timezone.now)
    logout_time = factory.LazyFunction(timezone.now)
    user_agent = factory.LazyAttribute(lambda _: fake.text())
    was_successful = factory.LazyAttribute(lambda _: fake.boolean())
    session_key = factory.LazyAttribute(lambda _: fake.word())

