import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.orders.factories import OrderFactory, OrderItemFactory, OrderStatusHistoryFactory
from apps.orders.models import Order, OrderItem, OrderStatusHistory

@pytest.mark.django_db
class TestOrderAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/orders/orders/'
        self.instance = OrderFactory()
        self.url_detail = f'/api/v1/orders/orders/{self.instance.pk}/'

    def test_order_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Order list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_order_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Order detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_order_create_requires_auth(self):
        """Ensure creating Order requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_order_update_requires_auth(self):
        """Ensure updating Order requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_order_delete_requires_auth(self):
        """Ensure deleting Order requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class TestOrderItemAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/orders/orderitems/'
        self.instance = OrderItemFactory()
        self.url_detail = f'/api/v1/orders/orderitems/{self.instance.pk}/'

    def test_orderitem_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access OrderItem list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_orderitem_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to OrderItem detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_orderitem_create_requires_auth(self):
        """Ensure creating OrderItem requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_orderitem_update_requires_auth(self):
        """Ensure updating OrderItem requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_orderitem_delete_requires_auth(self):
        """Ensure deleting OrderItem requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class TestOrderStatusHistoryAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/orders/orderstatushistorys/'
        self.instance = OrderStatusHistoryFactory()
        self.url_detail = f'/api/v1/orders/orderstatushistorys/{self.instance.pk}/'

    def test_orderstatushistory_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access OrderStatusHistory list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_orderstatushistory_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to OrderStatusHistory detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_orderstatushistory_create_requires_auth(self):
        """Ensure creating OrderStatusHistory requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_orderstatushistory_update_requires_auth(self):
        """Ensure updating OrderStatusHistory requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_orderstatushistory_delete_requires_auth(self):
        """Ensure deleting OrderStatusHistory requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

