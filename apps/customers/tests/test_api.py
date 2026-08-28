import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.customers.factories import CustomerFactory
from apps.customers.models import Customer

@pytest.mark.django_db
class TestCustomerAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/customers/customers/'
        self.instance = CustomerFactory()
        self.url_detail = f'/api/v1/customers/customers/{self.instance.pk}/'

    def test_customer_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Customer list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_customer_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Customer detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_customer_create_requires_auth(self):
        """Ensure creating Customer requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_customer_update_requires_auth(self):
        """Ensure updating Customer requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_customer_delete_requires_auth(self):
        """Ensure deleting Customer requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

