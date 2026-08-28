import factory
from django.utils import timezone
from faker import Faker
from .models import FraudAnalysis

fake = Faker()

class FraudAnalysisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FraudAnalysis

    anomaly_score = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    risk_level = factory.LazyAttribute(lambda _: fake.word())
    is_flagged = factory.LazyAttribute(lambda _: fake.boolean())
    reviewed = factory.LazyAttribute(lambda _: fake.boolean())
    notes = factory.LazyAttribute(lambda _: fake.text())
    created_at = factory.LazyFunction(timezone.now)

