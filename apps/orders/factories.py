import factory
from django.utils import timezone
from faker import Faker
from .models import Order, OrderItem, OrderStatusHistory

fake = Faker()

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    order_number = factory.LazyAttribute(lambda _: fake.word())
    status = factory.LazyAttribute(lambda _: fake.word())
    subtotal = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    discount_amount = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    shipping_cost = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    tax_amount = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    total_amount = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    shipping_name = factory.LazyAttribute(lambda _: fake.name())
    shipping_phone = factory.LazyAttribute(lambda _: fake.word())
    shipping_city = factory.LazyAttribute(lambda _: fake.word())
    shipping_state = factory.LazyAttribute(lambda _: fake.word())
    shipping_pincode = factory.LazyAttribute(lambda _: fake.word())
    shipping_country = factory.LazyAttribute(lambda _: fake.word())
    customer_notes = factory.LazyAttribute(lambda _: fake.text())
    admin_notes = factory.LazyAttribute(lambda _: fake.text())
    tracking_number = factory.LazyAttribute(lambda _: fake.word())
    estimated_delivery = factory.LazyFunction(timezone.now)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    delivered_at = factory.LazyFunction(timezone.now)
    cancelled_at = factory.LazyFunction(timezone.now)

class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    product_name = factory.LazyAttribute(lambda _: fake.name())
    product_sku = factory.LazyAttribute(lambda _: fake.word())
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    unit_price = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    discount_amount = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    total_price = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))

class OrderStatusHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderStatusHistory

    old_status = factory.LazyAttribute(lambda _: fake.word())
    new_status = factory.LazyAttribute(lambda _: fake.word())
    note = factory.LazyAttribute(lambda _: fake.text())
    created_at = factory.LazyFunction(timezone.now)

