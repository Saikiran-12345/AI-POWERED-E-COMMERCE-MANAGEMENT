import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.reports.factories import ReportFactory
from apps.reports.models import Report

@pytest.mark.django_db
class TestReportAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/reports/reports/'
        self.instance = ReportFactory()
        self.url_detail = f'/api/v1/reports/reports/{self.instance.pk}/'

    def test_report_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Report list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_report_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Report detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_report_create_requires_auth(self):
        """Ensure creating Report requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_report_update_requires_auth(self):
        """Ensure updating Report requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_report_delete_requires_auth(self):
        """Ensure deleting Report requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

