import factory
from django.utils import timezone
from faker import Faker
from .models import Report

fake = Faker()

class ReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Report

    name = factory.LazyAttribute(lambda _: fake.name())
    report_type = factory.LazyAttribute(lambda _: fake.word())
    created_at = factory.LazyFunction(timezone.now)

