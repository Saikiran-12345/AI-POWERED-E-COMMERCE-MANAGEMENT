import factory
from django.utils import timezone
from faker import Faker
from .models import DemandForecast

fake = Faker()

class DemandForecastFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DemandForecast

    forecast_date = factory.LazyFunction(timezone.now)
    predicted_quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    confidence = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    model_version = factory.LazyAttribute(lambda _: fake.word())
    created_at = factory.LazyFunction(timezone.now)

