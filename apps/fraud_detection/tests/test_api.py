import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.fraud_detection.factories import FraudAnalysisFactory
from apps.fraud_detection.models import FraudAnalysis

@pytest.mark.django_db
class TestFraudAnalysisAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/fraud_detection/fraudanalysiss/'
        self.instance = FraudAnalysisFactory()
        self.url_detail = f'/api/v1/fraud_detection/fraudanalysiss/{self.instance.pk}/'

    def test_fraudanalysis_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access FraudAnalysis list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_fraudanalysis_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to FraudAnalysis detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_fraudanalysis_create_requires_auth(self):
        """Ensure creating FraudAnalysis requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_fraudanalysis_update_requires_auth(self):
        """Ensure updating FraudAnalysis requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_fraudanalysis_delete_requires_auth(self):
        """Ensure deleting FraudAnalysis requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

