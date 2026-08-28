import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.forecasting.models import DemandForecast
from apps.forecasting.factories import DemandForecastFactory

@pytest.mark.django_db
class TestDemandForecastModel(TestCase):
    def setUp(self):
        self.instance = DemandForecastFactory()

    def test_demandforecast_creation(self):
        """Test that DemandForecast instance can be created and saved successfully."""
        self.assertIsNotNone(self.instance.pk)
        self.assertTrue(isinstance(self.instance, DemandForecast))

    def test_demandforecast_str_representation(self):
        """Test the string representation of DemandForecast."""
        self.assertIsInstance(str(self.instance), str)

    def test_demandforecast_product_field(self):
        """Ensure product field behaves correctly in DemandForecast."""
        field = DemandForecast._meta.get_field('product')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'product'))

    def test_demandforecast_category_field(self):
        """Ensure category field behaves correctly in DemandForecast."""
        field = DemandForecast._meta.get_field('category')
        self.assertEqual(field.get_internal_type(), 'ForeignKey')
        self.assertTrue(hasattr(self.instance, 'category'))

    def test_demandforecast_forecast_date_field(self):
        """Ensure forecast_date field behaves correctly in DemandForecast."""
        field = DemandForecast._meta.get_field('forecast_date')
        self.assertTrue(hasattr(self.instance, 'forecast_date'))

    def test_demandforecast_predicted_quantity_field(self):
        """Ensure predicted_quantity field behaves correctly in DemandForecast."""
        field = DemandForecast._meta.get_field('predicted_quantity')
        self.assertEqual(field.get_internal_type(), 'IntegerField')
        self.assertTrue(hasattr(self.instance, 'predicted_quantity'))

    def test_demandforecast_confidence_field(self):
        """Ensure confidence field behaves correctly in DemandForecast."""
        field = DemandForecast._meta.get_field('confidence')
        self.assertTrue(hasattr(self.instance, 'confidence'))

    def test_demandforecast_model_version_field(self):
        """Ensure model_version field behaves correctly in DemandForecast."""
        field = DemandForecast._meta.get_field('model_version')
        self.assertEqual(field.get_internal_type(), 'CharField')
        self.assertTrue(hasattr(self.instance, 'model_version'))

    def test_demandforecast_created_at_field(self):
        """Ensure created_at field behaves correctly in DemandForecast."""
        field = DemandForecast._meta.get_field('created_at')
        self.assertTrue(hasattr(self.instance, 'created_at'))

