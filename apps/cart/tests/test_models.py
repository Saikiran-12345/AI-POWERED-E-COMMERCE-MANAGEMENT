import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.cart.models import Cart, CartItem
from apps.cart.factories import CartFactory, CartItemFactory

@pytest.mark.django_db
class TestCartModel(TestCase):
    def setUp(self):
        self.instance = CartFactory()

    def test_cart_creation(self):
        """Test that Cart instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Cart))

    def test_cart_str_representation(self):
        """Test the string representation of Cart."""
        self.assertIsInstance(str(self.instance), str)

    def test_cart_user_field(self):
        """Ensure user field behaves correctly in Cart."""
        field = Cart._meta.get_field('user')
        self.assertTrue(hasattr(self.instance, 'user'))

    def test_cart_session_key_field(self):
        """Ensure session_key field behaves correctly in Cart."""
        field = Cart._meta.get_field('session_key')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'session_key'))

    def test_cart_coupon_code_field(self):
        """Ensure coupon_code field behaves correctly in Cart."""
        field = Cart._meta.get_field('coupon_code')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'coupon_code'))

    def test_cart_discount_amount_field(self):
        """Ensure discount_amount field behaves correctly in Cart."""
        field = Cart._meta.get_field('discount_amount')
        self.assertTrue(hasattr(self.instance, 'discount_amount'))

    def test_cart_created_at_field(self):
        """Ensure created_at field behaves correctly in Cart."""
        field = Cart._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

    def test_cart_updated_at_field(self):
        """Ensure updated_at field behaves correctly in Cart."""
        field = Cart._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

class TestCartItemModel(TestCase):
    def setUp(self):
        self.instance = CartItemFactory()

    def test_cartitem_creation(self):
        """Test that CartItem instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, CartItem))

    def test_cartitem_str_representation(self):
        """Test the string representation of CartItem."""
        self.assertIsInstance(str(self.instance), str)

    def test_cartitem_cart_field(self):
        """Ensure cart field behaves correctly in CartItem."""
        field = CartItem._meta.get_field('cart')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'cart'))

    def test_cartitem_product_field(self):
        """Ensure product field behaves correctly in CartItem."""
        field = CartItem._meta.get_field('product')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'product'))

    def test_cartitem_quantity_field(self):
        """Ensure quantity field behaves correctly in CartItem."""
        field = CartItem._meta.get_field('quantity')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'quantity'))

    def test_cartitem_price_at_add_field(self):
        """Ensure price_at_add field behaves correctly in CartItem."""
        field = CartItem._meta.get_field('price_at_add')
        self.assertTrue(hasattr(self.instance, 'price_at_add'))

    def test_cartitem_added_at_field(self):
        """Ensure added_at field behaves correctly in CartItem."""
        field = CartItem._meta.get_field('added_at')
        self.assertTrue(hasattr(self.instance, 'added_at'))

    def test_cartitem_updated_at_field(self):
        """Ensure updated_at field behaves correctly in CartItem."""
        field = CartItem._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

