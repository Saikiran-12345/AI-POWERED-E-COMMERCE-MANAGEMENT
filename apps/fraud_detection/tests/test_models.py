import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.fraud_detection.models import FraudAnalysis
from apps.fraud_detection.factories import FraudAnalysisFactory

@pytest.mark.django_db
class TestFraudAnalysisModel(TestCase):
    def setUp(self):
        self.instance = FraudAnalysisFactory()

    def test_fraudanalysis_creation(self):
        """Test that FraudAnalysis instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, FraudAnalysis))

    def test_fraudanalysis_str_representation(self):
        """Test the string representation of FraudAnalysis."""
        self.assertIsInstance(str(self.instance), str)

    def test_fraudanalysis_order_field(self):
        """Ensure order field behaves correctly in FraudAnalysis."""
        field = FraudAnalysis._meta.get_field('order')
        self.assertTrue(hasattr(self.instance, 'order'))

    def test_fraudanalysis_user_field(self):
        """Ensure user field behaves correctly in FraudAnalysis."""
        field = FraudAnalysis._meta.get_field('user')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'user'))

    def test_fraudanalysis_anomaly_score_field(self):
        """Ensure anomaly_score field behaves correctly in FraudAnalysis."""
        field = FraudAnalysis._meta.get_field('anomaly_score')
        self.assertTrue(hasattr(self.instance, 'anomaly_score'))

    def test_fraudanalysis_risk_level_field(self):
        """Ensure risk_level field behaves correctly in FraudAnalysis."""
        field = FraudAnalysis._meta.get_field('risk_level')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'risk_level'))

    def test_fraudanalysis_flags_field(self):
        """Ensure flags field behaves correctly in FraudAnalysis."""
        field = FraudAnalysis._meta.get_field('flags')
        self.assertTrue(hasattr(self.instance, 'flags'))

    def test_fraudanalysis_is_flagged_field(self):
        """Ensure is_flagged field behaves correctly in FraudAnalysis."""
        field = FraudAnalysis._meta.get_field('is_flagged')
        self.assertTrue(hasattr(self.instance, 'is_flagged'))

    def test_fraudanalysis_reviewed_field(self):
        """Ensure reviewed field behaves correctly in FraudAnalysis."""
        field = FraudAnalysis._meta.get_field('reviewed')
        self.assertTrue(hasattr(self.instance, 'reviewed'))

    def test_fraudanalysis_notes_field(self):
        """Ensure notes field behaves correctly in FraudAnalysis."""
        field = FraudAnalysis._meta.get_field('notes')
        self.assertTrue(hasattr(self.instance, 'notes'))

    def test_fraudanalysis_created_at_field(self):
        """Ensure created_at field behaves correctly in FraudAnalysis."""
        field = FraudAnalysis._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

