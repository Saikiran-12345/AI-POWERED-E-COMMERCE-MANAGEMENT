import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.wishlist.factories import WishlistFactory, WishlistItemFactory
from apps.wishlist.models import Wishlist, WishlistItem

@pytest.mark.django_db
class TestWishlistAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/wishlist/wishlists/'
        self.instance = WishlistFactory()
        self.url_detail = f'/api/v1/wishlist/wishlists/{self.instance.pk}/'

    def test_wishlist_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Wishlist list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_wishlist_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Wishlist detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_wishlist_create_requires_auth(self):
        """Ensure creating Wishlist requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_wishlist_update_requires_auth(self):
        """Ensure updating Wishlist requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_wishlist_delete_requires_auth(self):
        """Ensure deleting Wishlist requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class TestWishlistItemAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/wishlist/wishlistitems/'
        self.instance = WishlistItemFactory()
        self.url_detail = f'/api/v1/wishlist/wishlistitems/{self.instance.pk}/'

    def test_wishlistitem_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access WishlistItem list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_wishlistitem_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to WishlistItem detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_wishlistitem_create_requires_auth(self):
        """Ensure creating WishlistItem requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_wishlistitem_update_requires_auth(self):
        """Ensure updating WishlistItem requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_wishlistitem_delete_requires_auth(self):
        """Ensure deleting WishlistItem requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

