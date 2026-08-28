import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.recommendations.models import Recommendation
from apps.recommendations.factories import RecommendationFactory

@pytest.mark.django_db
class TestRecommendationModel(TestCase):
    def setUp(self):
        self.instance = RecommendationFactory()

    def test_recommendation_creation(self):
        """Test that Recommendation instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Recommendation))

    def test_recommendation_str_representation(self):
        """Test the string representation of Recommendation."""
        self.assertIsInstance(str(self.instance), str)

    def test_recommendation_user_field(self):
        """Ensure user field behaves correctly in Recommendation."""
        field = Recommendation._meta.get_field('user')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'user'))

    def test_recommendation_product_field(self):
        """Ensure product field behaves correctly in Recommendation."""
        field = Recommendation._meta.get_field('product')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'product'))

    def test_recommendation_score_field(self):
        """Ensure score field behaves correctly in Recommendation."""
        field = Recommendation._meta.get_field('score')
        self.assertTrue(hasattr(self.instance, 'score'))

    def test_recommendation_reason_field(self):
        """Ensure reason field behaves correctly in Recommendation."""
        field = Recommendation._meta.get_field('reason')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'reason'))

    def test_recommendation_created_at_field(self):
        """Ensure created_at field behaves correctly in Recommendation."""
        field = Recommendation._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

