import factory
from django.utils import timezone
from faker import Faker
from .models import Cart, CartItem

fake = Faker()

class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    session_key = factory.LazyAttribute(lambda _: fake.word())
    coupon_code = factory.LazyAttribute(lambda _: fake.word())
    discount_amount = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    price_at_add = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    added_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

