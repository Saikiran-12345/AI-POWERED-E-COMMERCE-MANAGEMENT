import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.analytics.models import SalesRecord
from apps.analytics.factories import SalesRecordFactory

@pytest.mark.django_db
class TestSalesRecordModel(TestCase):
    def setUp(self):
        self.instance = SalesRecordFactory()

    def test_salesrecord_creation(self):
        """Test that SalesRecord instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, SalesRecord))

    def test_salesrecord_str_representation(self):
        """Test the string representation of SalesRecord."""
        self.assertIsInstance(str(self.instance), str)

    def test_salesrecord_date_field(self):
        """Ensure date field behaves correctly in SalesRecord."""
        field = SalesRecord._meta.get_field('date')
        self.assertTrue(hasattr(self.instance, 'date'))

    def test_salesrecord_product_field(self):
        """Ensure product field behaves correctly in SalesRecord."""
        field = SalesRecord._meta.get_field('product')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'product'))

    def test_salesrecord_category_field(self):
        """Ensure category field behaves correctly in SalesRecord."""
        field = SalesRecord._meta.get_field('category')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'category'))

    def test_salesrecord_seller_field(self):
        """Ensure seller field behaves correctly in SalesRecord."""
        field = SalesRecord._meta.get_field('seller')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'seller'))

    def test_salesrecord_quantity_field(self):
        """Ensure quantity field behaves correctly in SalesRecord."""
        field = SalesRecord._meta.get_field('quantity')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'quantity'))

    def test_salesrecord_revenue_field(self):
        """Ensure revenue field behaves correctly in SalesRecord."""
        field = SalesRecord._meta.get_field('revenue')
        self.assertTrue(hasattr(self.instance, 'revenue'))

    def test_salesrecord_order_field(self):
        """Ensure order field behaves correctly in SalesRecord."""
        field = SalesRecord._meta.get_field('order')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'order'))

    def test_salesrecord_created_at_field(self):
        """Ensure created_at field behaves correctly in SalesRecord."""
        field = SalesRecord._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

