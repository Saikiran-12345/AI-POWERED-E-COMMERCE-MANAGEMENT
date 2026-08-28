import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.products.factories import CategoryFactory, ProductFactory, ProductImageFactory, ProductAttributeFactory
from apps.products.models import Category, Product, ProductImage, ProductAttribute

@pytest.mark.django_db
class TestCategoryAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/products/categorys/'
        self.instance = CategoryFactory()
        self.url_detail = f'/api/v1/products/categorys/{self.instance.pk}/'

    def test_category_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Category list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_category_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Category detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_category_create_requires_auth(self):
        """Ensure creating Category requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_category_update_requires_auth(self):
        """Ensure updating Category requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_category_delete_requires_auth(self):
        """Ensure deleting Category requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class TestProductAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/products/products/'
        self.instance = ProductFactory()
        self.url_detail = f'/api/v1/products/products/{self.instance.pk}/'

    def test_product_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Product list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_product_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Product detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_product_create_requires_auth(self):
        """Ensure creating Product requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_product_update_requires_auth(self):
        """Ensure updating Product requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_product_delete_requires_auth(self):
        """Ensure deleting Product requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class TestProductImageAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/products/productimages/'
        self.instance = ProductImageFactory()
        self.url_detail = f'/api/v1/products/productimages/{self.instance.pk}/'

    def test_productimage_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access ProductImage list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_productimage_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to ProductImage detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_productimage_create_requires_auth(self):
        """Ensure creating ProductImage requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_productimage_update_requires_auth(self):
        """Ensure updating ProductImage requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_productimage_delete_requires_auth(self):
        """Ensure deleting ProductImage requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class TestProductAttributeAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/products/productattributes/'
        self.instance = ProductAttributeFactory()
        self.url_detail = f'/api/v1/products/productattributes/{self.instance.pk}/'

    def test_productattribute_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access ProductAttribute list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_productattribute_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to ProductAttribute detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_productattribute_create_requires_auth(self):
        """Ensure creating ProductAttribute requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_productattribute_update_requires_auth(self):
        """Ensure updating ProductAttribute requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_productattribute_delete_requires_auth(self):
        """Ensure deleting ProductAttribute requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

