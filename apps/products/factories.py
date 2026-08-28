import factory
from django.utils import timezone
from faker import Faker
from .models import Category, Product, ProductImage, ProductAttribute

fake = Faker()

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: fake.name())
    description = factory.LazyAttribute(lambda _: fake.text())
    is_active = factory.LazyAttribute(lambda _: fake.boolean())
    sort_order = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda _: fake.name())
    description = factory.LazyAttribute(lambda _: fake.text())
    short_description = factory.LazyAttribute(lambda _: fake.word())
    brand = factory.LazyAttribute(lambda _: fake.word())
    sku = factory.LazyAttribute(lambda _: fake.word())
    price = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    discount_percent = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    cost_price = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    status = factory.LazyAttribute(lambda _: fake.word())
    is_featured = factory.LazyAttribute(lambda _: fake.boolean())
    is_digital = factory.LazyAttribute(lambda _: fake.boolean())
    average_rating = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    review_count = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    meta_title = factory.LazyAttribute(lambda _: fake.word())
    meta_description = factory.LazyAttribute(lambda _: fake.word())
    tags = factory.LazyAttribute(lambda _: fake.word())
    view_count = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    purchase_count = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alt_text = factory.LazyAttribute(lambda _: fake.word())
    sort_order = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    created_at = factory.LazyFunction(timezone.now)

class ProductAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttribute

    name = factory.LazyAttribute(lambda _: fake.name())
    value = factory.LazyAttribute(lambda _: fake.word())

