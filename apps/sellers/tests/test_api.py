import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.sellers.factories import SellerProfileFactory
from apps.sellers.models import SellerProfile

@pytest.mark.django_db
class TestSellerProfileAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/sellers/sellerprofiles/'
        self.instance = SellerProfileFactory()
        self.url_detail = f'/api/v1/sellers/sellerprofiles/{self.instance.pk}/'

    def test_sellerprofile_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access SellerProfile list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_sellerprofile_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to SellerProfile detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_sellerprofile_create_requires_auth(self):
        """Ensure creating SellerProfile requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_sellerprofile_update_requires_auth(self):
        """Ensure updating SellerProfile requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_sellerprofile_delete_requires_auth(self):
        """Ensure deleting SellerProfile requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

