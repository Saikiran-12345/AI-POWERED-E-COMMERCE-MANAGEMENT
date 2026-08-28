import factory
from django.utils import timezone
from faker import Faker
from .models import Recommendation

fake = Faker()

class RecommendationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recommendation

    score = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))
    reason = factory.LazyAttribute(lambda _: fake.word())
    created_at = factory.LazyFunction(timezone.now)

