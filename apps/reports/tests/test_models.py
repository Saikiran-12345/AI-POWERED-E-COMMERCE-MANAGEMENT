import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.reports.models import Report
from apps.reports.factories import ReportFactory

@pytest.mark.django_db
class TestReportModel(TestCase):
    def setUp(self):
        self.instance = ReportFactory()

    def test_report_creation(self):
        """Test that Report instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, Report))

    def test_report_str_representation(self):
        """Test the string representation of Report."""
        self.assertIsInstance(str(self.instance), str)

    def test_report_name_field(self):
        """Ensure name field behaves correctly in Report."""
        field = Report._meta.get_field('name')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'name'))

    def test_report_report_type_field(self):
        """Ensure report_type field behaves correctly in Report."""
        field = Report._meta.get_field('report_type')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'report_type'))

    def test_report_parameters_field(self):
        """Ensure parameters field behaves correctly in Report."""
        field = Report._meta.get_field('parameters')
        self.assertTrue(hasattr(self.instance, 'parameters'))

    def test_report_generated_by_field(self):
        """Ensure generated_by field behaves correctly in Report."""
        field = Report._meta.get_field('generated_by')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'generated_by'))

    def test_report_created_at_field(self):
        """Ensure created_at field behaves correctly in Report."""
        field = Report._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

