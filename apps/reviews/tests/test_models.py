import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.reviews.models import Review
from apps.reviews.factories import ReviewFactory

@pytest.mark.django_db
class TestReviewModel(TestCase):
    def setUp(self):
        self.instance = ReviewFactory()

    def test_review_creation(self):
        """Test that Review instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Review))

    def test_review_str_representation(self):
        """Test the string representation of Review."""
        self.assertIsInstance(str(self.instance), str)

    def test_review_product_field(self):
        """Ensure product field behaves correctly in Review."""
        field = Review._meta.get_field('product')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'product'))

    def test_review_customer_field(self):
        """Ensure customer field behaves correctly in Review."""
        field = Review._meta.get_field('customer')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'customer'))

    def test_review_rating_field(self):
        """Ensure rating field behaves correctly in Review."""
        field = Review._meta.get_field('rating')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'rating'))

    def test_review_title_field(self):
        """Ensure title field behaves correctly in Review."""
        field = Review._meta.get_field('title')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'title'))

    def test_review_body_field(self):
        """Ensure body field behaves correctly in Review."""
        field = Review._meta.get_field('body')
        self.assertTrue(hasattr(self.instance, 'body'))

    def test_review_is_approved_field(self):
        """Ensure is_approved field behaves correctly in Review."""
        field = Review._meta.get_field('is_approved')
        self.assertTrue(hasattr(self.instance, 'is_approved'))

    def test_review_is_verified_purchase_field(self):
        """Ensure is_verified_purchase field behaves correctly in Review."""
        field = Review._meta.get_field('is_verified_purchase')
        self.assertTrue(hasattr(self.instance, 'is_verified_purchase'))

    def test_review_helpful_count_field(self):
        """Ensure helpful_count field behaves correctly in Review."""
        field = Review._meta.get_field('helpful_count')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'helpful_count'))

    def test_review_created_at_field(self):
        """Ensure created_at field behaves correctly in Review."""
        field = Review._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

    def test_review_updated_at_field(self):
        """Ensure updated_at field behaves correctly in Review."""
        field = Review._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

