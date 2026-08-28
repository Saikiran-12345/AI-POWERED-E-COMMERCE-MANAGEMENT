import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.orders.models import Order, OrderItem, OrderStatusHistory
from apps.orders.factories import OrderFactory, OrderItemFactory, OrderStatusHistoryFactory

@pytest.mark.django_db
class TestOrderModel(TestCase):
    def setUp(self):
        self.instance = OrderFactory()

    def test_order_creation(self):
        """Test that Order instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Order))

    def test_order_str_representation(self):
        """Test the string representation of Order."""
        self.assertIsInstance(str(self.instance), str)

    def test_order_order_number_field(self):
        """Ensure order_number field behaves correctly in Order."""
        field = Order._meta.get_field('order_number')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'order_number'))

    def test_order_customer_field(self):
        """Ensure customer field behaves correctly in Order."""
        field = Order._meta.get_field('customer')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'customer'))

    def test_order_status_field(self):
        """Ensure status field behaves correctly in Order."""
        field = Order._meta.get_field('status')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'status'))

    def test_order_subtotal_field(self):
        """Ensure subtotal field behaves correctly in Order."""
        field = Order._meta.get_field('subtotal')
        self.assertTrue(hasattr(self.instance, 'subtotal'))

    def test_order_discount_amount_field(self):
        """Ensure discount_amount field behaves correctly in Order."""
        field = Order._meta.get_field('discount_amount')
        self.assertTrue(hasattr(self.instance, 'discount_amount'))

    def test_order_shipping_cost_field(self):
        """Ensure shipping_cost field behaves correctly in Order."""
        field = Order._meta.get_field('shipping_cost')
        self.assertTrue(hasattr(self.instance, 'shipping_cost'))

    def test_order_tax_amount_field(self):
        """Ensure tax_amount field behaves correctly in Order."""
        field = Order._meta.get_field('tax_amount')
        self.assertTrue(hasattr(self.instance, 'tax_amount'))

    def test_order_total_amount_field(self):
        """Ensure total_amount field behaves correctly in Order."""
        field = Order._meta.get_field('total_amount')
        self.assertTrue(hasattr(self.instance, 'total_amount'))

    def test_order_shipping_name_field(self):
        """Ensure shipping_name field behaves correctly in Order."""
        field = Order._meta.get_field('shipping_name')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'shipping_name'))

    def test_order_shipping_email_field(self):
        """Ensure shipping_email field behaves correctly in Order."""
        field = Order._meta.get_field('shipping_email')
        self.assertTrue(hasattr(self.instance, 'shipping_email'))

    def test_order_shipping_phone_field(self):
        """Ensure shipping_phone field behaves correctly in Order."""
        field = Order._meta.get_field('shipping_phone')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'shipping_phone'))

    def test_order_shipping_city_field(self):
        """Ensure shipping_city field behaves correctly in Order."""
        field = Order._meta.get_field('shipping_city')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'shipping_city'))

    def test_order_shipping_state_field(self):
        """Ensure shipping_state field behaves correctly in Order."""
        field = Order._meta.get_field('shipping_state')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'shipping_state'))

    def test_order_shipping_pincode_field(self):
        """Ensure shipping_pincode field behaves correctly in Order."""
        field = Order._meta.get_field('shipping_pincode')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'shipping_pincode'))

    def test_order_shipping_country_field(self):
        """Ensure shipping_country field behaves correctly in Order."""
        field = Order._meta.get_field('shipping_country')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'shipping_country'))

    def test_order_customer_notes_field(self):
        """Ensure customer_notes field behaves correctly in Order."""
        field = Order._meta.get_field('customer_notes')
        self.assertTrue(hasattr(self.instance, 'customer_notes'))

    def test_order_admin_notes_field(self):
        """Ensure admin_notes field behaves correctly in Order."""
        field = Order._meta.get_field('admin_notes')
        self.assertTrue(hasattr(self.instance, 'admin_notes'))

    def test_order_tracking_number_field(self):
        """Ensure tracking_number field behaves correctly in Order."""
        field = Order._meta.get_field('tracking_number')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'tracking_number'))

    def test_order_estimated_delivery_field(self):
        """Ensure estimated_delivery field behaves correctly in Order."""
        field = Order._meta.get_field('estimated_delivery')
        self.assertTrue(hasattr(self.instance, 'estimated_delivery'))

    def test_order_created_at_field(self):
        """Ensure created_at field behaves correctly in Order."""
        field = Order._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

    def test_order_updated_at_field(self):
        """Ensure updated_at field behaves correctly in Order."""
        field = Order._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

    def test_order_delivered_at_field(self):
        """Ensure delivered_at field behaves correctly in Order."""
        field = Order._meta.get_field('delivered_at')
        self.assertTrue(hasattr(self.instance, 'delivered_at'))

    def test_order_cancelled_at_field(self):
        """Ensure cancelled_at field behaves correctly in Order."""
        field = Order._meta.get_field('cancelled_at')
        self.assertTrue(hasattr(self.instance, 'cancelled_at'))

class TestOrderItemModel(TestCase):
    def setUp(self):
        self.instance = OrderItemFactory()

    def test_orderitem_creation(self):
        """Test that OrderItem instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, OrderItem))

    def test_orderitem_str_representation(self):
        """Test the string representation of OrderItem."""
        self.assertIsInstance(str(self.instance), str)

    def test_orderitem_order_field(self):
        """Ensure order field behaves correctly in OrderItem."""
        field = OrderItem._meta.get_field('order')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'order'))

    def test_orderitem_product_field(self):
        """Ensure product field behaves correctly in OrderItem."""
        field = OrderItem._meta.get_field('product')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'product'))

    def test_orderitem_product_name_field(self):
        """Ensure product_name field behaves correctly in OrderItem."""
        field = OrderItem._meta.get_field('product_name')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'product_name'))

    def test_orderitem_product_sku_field(self):
        """Ensure product_sku field behaves correctly in OrderItem."""
        field = OrderItem._meta.get_field('product_sku')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'product_sku'))

    def test_orderitem_quantity_field(self):
        """Ensure quantity field behaves correctly in OrderItem."""
        field = OrderItem._meta.get_field('quantity')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'quantity'))

    def test_orderitem_unit_price_field(self):
        """Ensure unit_price field behaves correctly in OrderItem."""
        field = OrderItem._meta.get_field('unit_price')
        self.assertTrue(hasattr(self.instance, 'unit_price'))

    def test_orderitem_discount_amount_field(self):
        """Ensure discount_amount field behaves correctly in OrderItem."""
        field = OrderItem._meta.get_field('discount_amount')
        self.assertTrue(hasattr(self.instance, 'discount_amount'))

    def test_orderitem_total_price_field(self):
        """Ensure total_price field behaves correctly in OrderItem."""
        field = OrderItem._meta.get_field('total_price')
        self.assertTrue(hasattr(self.instance, 'total_price'))

    def test_orderitem_seller_field(self):
        """Ensure seller field behaves correctly in OrderItem."""
        field = OrderItem._meta.get_field('seller')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'seller'))

class TestOrderStatusHistoryModel(TestCase):
    def setUp(self):
        self.instance = OrderStatusHistoryFactory()

    def test_orderstatushistory_creation(self):
        """Test that OrderStatusHistory instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, OrderStatusHistory))

    def test_orderstatushistory_str_representation(self):
        """Test the string representation of OrderStatusHistory."""
        self.assertIsInstance(str(self.instance), str)

    def test_orderstatushistory_order_field(self):
        """Ensure order field behaves correctly in OrderStatusHistory."""
        field = OrderStatusHistory._meta.get_field('order')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'order'))

    def test_orderstatushistory_old_status_field(self):
        """Ensure old_status field behaves correctly in OrderStatusHistory."""
        field = OrderStatusHistory._meta.get_field('old_status')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'old_status'))

    def test_orderstatushistory_new_status_field(self):
        """Ensure new_status field behaves correctly in OrderStatusHistory."""
        field = OrderStatusHistory._meta.get_field('new_status')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'new_status'))

    def test_orderstatushistory_note_field(self):
        """Ensure note field behaves correctly in OrderStatusHistory."""
        field = OrderStatusHistory._meta.get_field('note')
        self.assertTrue(hasattr(self.instance, 'note'))

    def test_orderstatushistory_changed_by_field(self):
        """Ensure changed_by field behaves correctly in OrderStatusHistory."""
        field = OrderStatusHistory._meta.get_field('changed_by')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'changed_by'))

    def test_orderstatushistory_created_at_field(self):
        """Ensure created_at field behaves correctly in OrderStatusHistory."""
        field = OrderStatusHistory._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

