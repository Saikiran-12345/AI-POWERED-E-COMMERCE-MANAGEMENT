import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.notifications.models import Notification
from apps.notifications.factories import NotificationFactory

@pytest.mark.django_db
class TestNotificationModel(TestCase):
    def setUp(self):
        self.instance = NotificationFactory()

    def test_notification_creation(self):
        """Test that Notification instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Notification))

    def test_notification_str_representation(self):
        """Test the string representation of Notification."""
        self.assertIsInstance(str(self.instance), str)

    def test_notification_user_field(self):
        """Ensure user field behaves correctly in Notification."""
        field = Notification._meta.get_field('user')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'user'))

    def test_notification_notification_type_field(self):
        """Ensure notification_type field behaves correctly in Notification."""
        field = Notification._meta.get_field('notification_type')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'notification_type'))

    def test_notification_title_field(self):
        """Ensure title field behaves correctly in Notification."""
        field = Notification._meta.get_field('title')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'title'))

    def test_notification_message_field(self):
        """Ensure message field behaves correctly in Notification."""
        field = Notification._meta.get_field('message')
        self.assertTrue(hasattr(self.instance, 'message'))

    def test_notification_link_field(self):
        """Ensure link field behaves correctly in Notification."""
        field = Notification._meta.get_field('link')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'link'))

    def test_notification_is_read_field(self):
        """Ensure is_read field behaves correctly in Notification."""
        field = Notification._meta.get_field('is_read')
        self.assertTrue(hasattr(self.instance, 'is_read'))

    def test_notification_created_at_field(self):
        """Ensure created_at field behaves correctly in Notification."""
        field = Notification._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

