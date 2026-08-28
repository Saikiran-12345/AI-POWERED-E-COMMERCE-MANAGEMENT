import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.accounts.models import UserProfile, LoginHistory
from apps.accounts.factories import UserProfileFactory, LoginHistoryFactory

@pytest.mark.django_db
class TestUserProfileModel(TestCase):
    def setUp(self):
        self.instance = UserProfileFactory()

    def test_userprofile_creation(self):
        """Test that UserProfile instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, UserProfile))

    def test_userprofile_str_representation(self):
        """Test the string representation of UserProfile."""
        self.assertIsInstance(str(self.instance), str)

    def test_userprofile_user_field(self):
        """Ensure user field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('user')
        self.assertTrue(hasattr(self.instance, 'user'))

    def test_userprofile_bio_field(self):
        """Ensure bio field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('bio')
        self.assertTrue(hasattr(self.instance, 'bio'))

    def test_userprofile_date_of_birth_field(self):
        """Ensure date_of_birth field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('date_of_birth')
        self.assertTrue(hasattr(self.instance, 'date_of_birth'))

    def test_userprofile_gender_field(self):
        """Ensure gender field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('gender')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'gender'))

    def test_userprofile_city_field(self):
        """Ensure city field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('city')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'city'))

    def test_userprofile_state_field(self):
        """Ensure state field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('state')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'state'))

    def test_userprofile_pincode_field(self):
        """Ensure pincode field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('pincode')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'pincode'))

    def test_userprofile_country_field(self):
        """Ensure country field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('country')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'country'))

    def test_userprofile_newsletter_subscribed_field(self):
        """Ensure newsletter_subscribed field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('newsletter_subscribed')
        self.assertTrue(hasattr(self.instance, 'newsletter_subscribed'))

    def test_userprofile_email_notifications_field(self):
        """Ensure email_notifications field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('email_notifications')
        self.assertTrue(hasattr(self.instance, 'email_notifications'))

    def test_userprofile_sms_notifications_field(self):
        """Ensure sms_notifications field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('sms_notifications')
        self.assertTrue(hasattr(self.instance, 'sms_notifications'))

    def test_userprofile_created_at_field(self):
        """Ensure created_at field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

    def test_userprofile_updated_at_field(self):
        """Ensure updated_at field behaves correctly in UserProfile."""
        field = UserProfile._meta.get_field('updated_at')
        self.assertTrue(hasattr(self.instance, 'updated_at'))

class TestLoginHistoryModel(TestCase):
    def setUp(self):
        self.instance = LoginHistoryFactory()

    def test_loginhistory_creation(self):
        """Test that LoginHistory instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, LoginHistory))

    def test_loginhistory_str_representation(self):
        """Test the string representation of LoginHistory."""
        self.assertIsInstance(str(self.instance), str)

    def test_loginhistory_user_field(self):
        """Ensure user field behaves correctly in LoginHistory."""
        field = LoginHistory._meta.get_field('user')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'user'))

    def test_loginhistory_login_time_field(self):
        """Ensure login_time field behaves correctly in LoginHistory."""
        field = LoginHistory._meta.get_field('login_time')
        self.assertTrue(hasattr(self.instance, 'login_time'))

    def test_loginhistory_logout_time_field(self):
        """Ensure logout_time field behaves correctly in LoginHistory."""
        field = LoginHistory._meta.get_field('logout_time')
        self.assertTrue(hasattr(self.instance, 'logout_time'))

    def test_loginhistory_ip_address_field(self):
        """Ensure ip_address field behaves correctly in LoginHistory."""
        field = LoginHistory._meta.get_field('ip_address')
        self.assertTrue(hasattr(self.instance, 'ip_address'))

    def test_loginhistory_user_agent_field(self):
        """Ensure user_agent field behaves correctly in LoginHistory."""
        field = LoginHistory._meta.get_field('user_agent')
        self.assertTrue(hasattr(self.instance, 'user_agent'))

    def test_loginhistory_was_successful_field(self):
        """Ensure was_successful field behaves correctly in LoginHistory."""
        field = LoginHistory._meta.get_field('was_successful')
        self.assertTrue(hasattr(self.instance, 'was_successful'))

    def test_loginhistory_session_key_field(self):
        """Ensure session_key field behaves correctly in LoginHistory."""
        field = LoginHistory._meta.get_field('session_key')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'session_key'))

