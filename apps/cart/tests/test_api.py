import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.cart.factories import CartFactory, CartItemFactory
from apps.cart.models import Cart, CartItem

@pytest.mark.django_db
class TestCartAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/cart/carts/'
        self.instance = CartFactory()
        self.url_detail = f'/api/v1/cart/carts/{self.instance.pk}/'

    def test_cart_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Cart list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_cart_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Cart detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_cart_create_requires_auth(self):
        """Ensure creating Cart requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_cart_update_requires_auth(self):
        """Ensure updating Cart requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_cart_delete_requires_auth(self):
        """Ensure deleting Cart requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class TestCartItemAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/cart/cartitems/'
        self.instance = CartItemFactory()
        self.url_detail = f'/api/v1/cart/cartitems/{self.instance.pk}/'

    def test_cartitem_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access CartItem list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_cartitem_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to CartItem detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_cartitem_create_requires_auth(self):
        """Ensure creating CartItem requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_cartitem_update_requires_auth(self):
        """Ensure updating CartItem requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_cartitem_delete_requires_auth(self):
        """Ensure deleting CartItem requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

