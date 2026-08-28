import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.wishlist.models import Wishlist, WishlistItem
from apps.wishlist.factories import WishlistFactory, WishlistItemFactory

@pytest.mark.django_db
class TestWishlistModel(TestCase):
    def setUp(self):
        self.instance = WishlistFactory()

    def test_wishlist_creation(self):
        """Test that Wishlist instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Wishlist))

    def test_wishlist_str_representation(self):
        """Test the string representation of Wishlist."""
        self.assertIsInstance(str(self.instance), str)

    def test_wishlist_customer_field(self):
        """Ensure customer field behaves correctly in Wishlist."""
        field = Wishlist._meta.get_field('customer')
        self.assertTrue(hasattr(self.instance, 'customer'))

    def test_wishlist_created_at_field(self):
        """Ensure created_at field behaves correctly in Wishlist."""
        field = Wishlist._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

    def test_wishlist_updated_at_field(self):
        """Ensure updated_at field behaves correctly in Wishlist."""
        field = Wishlist._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

class TestWishlistItemModel(TestCase):
    def setUp(self):
        self.instance = WishlistItemFactory()

    def test_wishlistitem_creation(self):
        """Test that WishlistItem instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, WishlistItem))

    def test_wishlistitem_str_representation(self):
        """Test the string representation of WishlistItem."""
        self.assertIsInstance(str(self.instance), str)

    def test_wishlistitem_wishlist_field(self):
        """Ensure wishlist field behaves correctly in WishlistItem."""
        field = WishlistItem._meta.get_field('wishlist')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'wishlist'))

    def test_wishlistitem_product_field(self):
        """Ensure product field behaves correctly in WishlistItem."""
        field = WishlistItem._meta.get_field('product')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'product'))

    def test_wishlistitem_added_at_field(self):
        """Ensure added_at field behaves correctly in WishlistItem."""
        field = WishlistItem._meta.get_field('added_at')
        self.assertTrue(hasattr(self.instance, 'added_at'))

