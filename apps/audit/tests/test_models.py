import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.audit.models import AuditLog
from apps.audit.factories import AuditLogFactory

@pytest.mark.django_db
class TestAuditLogModel(TestCase):
    def setUp(self):
        self.instance = AuditLogFactory()

    def test_auditlog_creation(self):
        """Test that AuditLog instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, AuditLog))

    def test_auditlog_str_representation(self):
        """Test the string representation of AuditLog."""
        self.assertIsInstance(str(self.instance), str)

    def test_auditlog_user_field(self):
        """Ensure user field behaves correctly in AuditLog."""
        field = AuditLog._meta.get_field('user')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'user'))

    def test_auditlog_action_field(self):
        """Ensure action field behaves correctly in AuditLog."""
        field = AuditLog._meta.get_field('action')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'action'))

    def test_auditlog_module_field(self):
        """Ensure module field behaves correctly in AuditLog."""
        field = AuditLog._meta.get_field('module')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'module'))

    def test_auditlog_description_field(self):
        """Ensure description field behaves correctly in AuditLog."""
        field = AuditLog._meta.get_field('description')
        self.assertTrue(hasattr(self.instance, 'description'))

    def test_auditlog_object_type_field(self):
        """Ensure object_type field behaves correctly in AuditLog."""
        field = AuditLog._meta.get_field('object_type')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'object_type'))

    def test_auditlog_object_id_field(self):
        """Ensure object_id field behaves correctly in AuditLog."""
        field = AuditLog._meta.get_field('object_id')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'object_id'))

    def test_auditlog_extra_data_field(self):
        """Ensure extra_data field behaves correctly in AuditLog."""
        field = AuditLog._meta.get_field('extra_data')
        self.assertTrue(hasattr(self.instance, 'extra_data'))

    def test_auditlog_ip_address_field(self):
        """Ensure ip_address field behaves correctly in AuditLog."""
        field = AuditLog._meta.get_field('ip_address')
        self.assertTrue(hasattr(self.instance, 'ip_address'))

    def test_auditlog_user_agent_field(self):
        """Ensure user_agent field behaves correctly in AuditLog."""
        field = AuditLog._meta.get_field('user_agent')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'user_agent'))

    def test_auditlog_timestamp_field(self):
        """Ensure timestamp field behaves correctly in AuditLog."""
        field = AuditLog._meta.get_field('timestamp')
        self.assertTrue(hasattr(self.instance, 'timestamp'))

