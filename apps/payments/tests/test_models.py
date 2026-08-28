import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.payments.models import Payment
from apps.payments.factories import PaymentFactory

@pytest.mark.django_db
class TestPaymentModel(TestCase):
    def setUp(self):
        self.instance = PaymentFactory()

    def test_payment_creation(self):
        """Test that Payment instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Payment))

    def test_payment_str_representation(self):
        """Test the string representation of Payment."""
        self.assertIsInstance(str(self.instance), str)

    def test_payment_payment_id_field(self):
        """Ensure payment_id field behaves correctly in Payment."""
        field = Payment._meta.get_field('payment_id')
        self.assertTrue(hasattr(self.instance, 'payment_id'))

    def test_payment_order_field(self):
        """Ensure order field behaves correctly in Payment."""
        field = Payment._meta.get_field('order')
        self.assertTrue(hasattr(self.instance, 'order'))

    def test_payment_amount_field(self):
        """Ensure amount field behaves correctly in Payment."""
        field = Payment._meta.get_field('amount')
        self.assertTrue(hasattr(self.instance, 'amount'))

    def test_payment_method_field(self):
        """Ensure method field behaves correctly in Payment."""
        field = Payment._meta.get_field('method')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'method'))

    def test_payment_status_field(self):
        """Ensure status field behaves correctly in Payment."""
        field = Payment._meta.get_field('status')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'status'))

    def test_payment_transaction_reference_field(self):
        """Ensure transaction_reference field behaves correctly in Payment."""
        field = Payment._meta.get_field('transaction_reference')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'transaction_reference'))

    def test_payment_gateway_response_field(self):
        """Ensure gateway_response field behaves correctly in Payment."""
        field = Payment._meta.get_field('gateway_response')
        self.assertTrue(hasattr(self.instance, 'gateway_response'))

    def test_payment_failure_reason_field(self):
        """Ensure failure_reason field behaves correctly in Payment."""
        field = Payment._meta.get_field('failure_reason')
        self.assertTrue(hasattr(self.instance, 'failure_reason'))

    def test_payment_card_type_field(self):
        """Ensure card_type field behaves correctly in Payment."""
        field = Payment._meta.get_field('card_type')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'card_type'))

    def test_payment_upi_id_field(self):
        """Ensure upi_id field behaves correctly in Payment."""
        field = Payment._meta.get_field('upi_id')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'upi_id'))

    def test_payment_created_at_field(self):
        """Ensure created_at field behaves correctly in Payment."""
        field = Payment._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

    def test_payment_updated_at_field(self):
        """Ensure updated_at field behaves correctly in Payment."""
        field = Payment._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

    def test_payment_completed_at_field(self):
        """Ensure completed_at field behaves correctly in Payment."""
        field = Payment._meta.get_field('completed_at')
        self.assertTrue(hasattr(self.instance, 'completed_at'))

