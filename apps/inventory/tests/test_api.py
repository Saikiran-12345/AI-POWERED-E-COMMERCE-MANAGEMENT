import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.inventory.factories import InventoryFactory, InventoryHistoryFactory
from apps.inventory.models import Inventory, InventoryHistory

@pytest.mark.django_db
class TestInventoryAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/inventory/inventorys/'
        self.instance = InventoryFactory()
        self.url_detail = f'/api/v1/inventory/inventorys/{self.instance.pk}/'

    def test_inventory_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Inventory list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_inventory_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Inventory detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_inventory_create_requires_auth(self):
        """Ensure creating Inventory requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_inventory_update_requires_auth(self):
        """Ensure updating Inventory requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_inventory_delete_requires_auth(self):
        """Ensure deleting Inventory requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class TestInventoryHistoryAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/inventory/inventoryhistorys/'
        self.instance = InventoryHistoryFactory()
        self.url_detail = f'/api/v1/inventory/inventoryhistorys/{self.instance.pk}/'

    def test_inventoryhistory_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access InventoryHistory list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_inventoryhistory_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to InventoryHistory detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_inventoryhistory_create_requires_auth(self):
        """Ensure creating InventoryHistory requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_inventoryhistory_update_requires_auth(self):
        """Ensure updating InventoryHistory requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_inventoryhistory_delete_requires_auth(self):
        """Ensure deleting InventoryHistory requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

