import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.customers.models import Customer
from apps.customers.factories import CustomerFactory

@pytest.mark.django_db
class TestCustomerModel(TestCase):
    def setUp(self):
        self.instance = CustomerFactory()

    def test_customer_creation(self):
        """Test that Customer instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Customer))

    def test_customer_str_representation(self):
        """Test the string representation of Customer."""
        self.assertIsInstance(str(self.instance), str)

    def test_customer_user_field(self):
        """Ensure user field behaves correctly in Customer."""
        field = Customer._meta.get_field('user')
        self.assertTrue(hasattr(self.instance, 'user'))

    def test_customer_loyalty_points_field(self):
        """Ensure loyalty_points field behaves correctly in Customer."""
        field = Customer._meta.get_field('loyalty_points')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'loyalty_points'))

    def test_customer_total_spent_field(self):
        """Ensure total_spent field behaves correctly in Customer."""
        field = Customer._meta.get_field('total_spent')
        self.assertTrue(hasattr(self.instance, 'total_spent'))

    def test_customer_order_count_field(self):
        """Ensure order_count field behaves correctly in Customer."""
        field = Customer._meta.get_field('order_count')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'order_count'))

    def test_customer_segment_field(self):
        """Ensure segment field behaves correctly in Customer."""
        field = Customer._meta.get_field('segment')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'segment'))

    def test_customer_churn_risk_field(self):
        """Ensure churn_risk field behaves correctly in Customer."""
        field = Customer._meta.get_field('churn_risk')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'churn_risk'))

    def test_customer_churn_score_field(self):
        """Ensure churn_score field behaves correctly in Customer."""
        field = Customer._meta.get_field('churn_score')
        self.assertTrue(hasattr(self.instance, 'churn_score'))

    def test_customer_referral_code_field(self):
        """Ensure referral_code field behaves correctly in Customer."""
        field = Customer._meta.get_field('referral_code')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'referral_code'))

    def test_customer_created_at_field(self):
        """Ensure created_at field behaves correctly in Customer."""
        field = Customer._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

    def test_customer_updated_at_field(self):
        """Ensure updated_at field behaves correctly in Customer."""
        field = Customer._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

    def test_customer_total_field(self):
        """Ensure total field behaves correctly in Customer."""
        field = Customer._meta.get_field('total')
        self.assertTrue(hasattr(self.instance, 'total'))

