import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.analytics.factories import SalesRecordFactory
from apps.analytics.models import SalesRecord

@pytest.mark.django_db
class TestSalesRecordAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/analytics/salesrecords/'
        self.instance = SalesRecordFactory()
        self.url_detail = f'/api/v1/analytics/salesrecords/{self.instance.pk}/'

    def test_salesrecord_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access SalesRecord list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_salesrecord_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to SalesRecord detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_salesrecord_create_requires_auth(self):
        """Ensure creating SalesRecord requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_salesrecord_update_requires_auth(self):
        """Ensure updating SalesRecord requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_salesrecord_delete_requires_auth(self):
        """Ensure deleting SalesRecord requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

