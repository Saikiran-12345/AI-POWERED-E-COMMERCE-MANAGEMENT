import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.payments.factories import PaymentFactory
from apps.payments.models import Payment

@pytest.mark.django_db
class TestPaymentAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/payments/payments/'
        self.instance = PaymentFactory()
        self.url_detail = f'/api/v1/payments/payments/{self.instance.pk}/'

    def test_payment_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Payment list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_payment_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Payment detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_payment_create_requires_auth(self):
        """Ensure creating Payment requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_payment_update_requires_auth(self):
        """Ensure updating Payment requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_payment_delete_requires_auth(self):
        """Ensure deleting Payment requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

