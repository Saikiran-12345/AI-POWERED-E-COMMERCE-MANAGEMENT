import factory
from django.utils import timezone
from faker import Faker
from .models import SellerProfile

fake = Faker()

class SellerProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SellerProfile

    business_name = factory.LazyAttribute(lambda _: fake.name())
    business_phone = factory.LazyAttribute(lambda _: fake.word())
    business_address = factory.LazyAttribute(lambda _: fake.text())
    gst_number = factory.LazyAttribute(lambda _: fake.word())
    pan_number = factory.LazyAttribute(lambda _: fake.word())
    bank_account = factory.LazyAttribute(lambda _: fake.word())
    ifsc_code = factory.LazyAttribute(lambda _: fake.word())
    verification_status = factory.LazyAttribute(lambda _: fake.word())
    commission_rate = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    total_sales = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    total_orders = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    rating = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    bio = factory.LazyAttribute(lambda _: fake.text())
    is_active = factory.LazyAttribute(lambda _: fake.boolean())
    joined_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

