import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.sellers.models import SellerProfile
from apps.sellers.factories import SellerProfileFactory

@pytest.mark.django_db
class TestSellerProfileModel(TestCase):
    def setUp(self):
        self.instance = SellerProfileFactory()

    def test_sellerprofile_creation(self):
        """Test that SellerProfile instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, SellerProfile))

    def test_sellerprofile_str_representation(self):
        """Test the string representation of SellerProfile."""
        self.assertIsInstance(str(self.instance), str)

    def test_sellerprofile_user_field(self):
        """Ensure user field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('user')
        self.assertTrue(hasattr(self.instance, 'user'))

    def test_sellerprofile_business_name_field(self):
        """Ensure business_name field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('business_name')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'business_name'))

    def test_sellerprofile_business_email_field(self):
        """Ensure business_email field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('business_email')
        self.assertTrue(hasattr(self.instance, 'business_email'))

    def test_sellerprofile_business_phone_field(self):
        """Ensure business_phone field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('business_phone')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'business_phone'))

    def test_sellerprofile_business_address_field(self):
        """Ensure business_address field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('business_address')
        self.assertTrue(hasattr(self.instance, 'business_address'))

    def test_sellerprofile_gst_number_field(self):
        """Ensure gst_number field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('gst_number')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'gst_number'))

    def test_sellerprofile_pan_number_field(self):
        """Ensure pan_number field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('pan_number')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'pan_number'))

    def test_sellerprofile_bank_account_field(self):
        """Ensure bank_account field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('bank_account')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'bank_account'))

    def test_sellerprofile_ifsc_code_field(self):
        """Ensure ifsc_code field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('ifsc_code')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'ifsc_code'))

    def test_sellerprofile_verification_status_field(self):
        """Ensure verification_status field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('verification_status')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'verification_status'))

    def test_sellerprofile_commission_rate_field(self):
        """Ensure commission_rate field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('commission_rate')
        self.assertTrue(hasattr(self.instance, 'commission_rate'))

    def test_sellerprofile_total_sales_field(self):
        """Ensure total_sales field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('total_sales')
        self.assertTrue(hasattr(self.instance, 'total_sales'))

    def test_sellerprofile_total_orders_field(self):
        """Ensure total_orders field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('total_orders')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'total_orders'))

    def test_sellerprofile_rating_field(self):
        """Ensure rating field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('rating')
        self.assertTrue(hasattr(self.instance, 'rating'))

    def test_sellerprofile_bio_field(self):
        """Ensure bio field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('bio')
        self.assertTrue(hasattr(self.instance, 'bio'))

    def test_sellerprofile_logo_field(self):
        """Ensure logo field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('logo')
        self.assertTrue(hasattr(self.instance, 'logo'))

    def test_sellerprofile_is_active_field(self):
        """Ensure is_active field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('is_active')
        self.assertTrue(hasattr(self.instance, 'is_active'))

    def test_sellerprofile_joined_at_field(self):
        """Ensure joined_at field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('joined_at')
        self.assertTrue(hasattr(self.instance, 'joined_at'))

    def test_sellerprofile_updated_at_field(self):
        """Ensure updated_at field behaves correctly in SellerProfile."""
        field = SellerProfile._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

