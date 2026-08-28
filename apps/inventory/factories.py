import factory
from django.utils import timezone
from faker import Faker
from .models import Inventory, InventoryHistory

fake = Faker()

class InventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inventory

    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    reserved_quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    reorder_point = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    reorder_quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    warehouse_location = factory.LazyAttribute(lambda _: fake.word())
    last_restocked_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    created_at = factory.LazyFunction(timezone.now)

class InventoryHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InventoryHistory

    change_type = factory.LazyAttribute(lambda _: fake.word())
    quantity_changed = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    quantity_before = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    quantity_after = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    note = factory.LazyAttribute(lambda _: fake.text())
    created_at = factory.LazyFunction(timezone.now)

