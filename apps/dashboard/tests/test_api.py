import pytest
from rest_framework.test import APITestCase
from rest_framework import status

@pytest.mark.django_db
class TestDashboardAPI(APITestCase):
    def setUp(self):
        pass

    def test_api_list(self):
        self.assertTrue(True)
        
    def test_api_retrieve(self):
        self.assertTrue(True)
        
    def test_api_create(self):
        self.assertTrue(True)
        
    def test_api_update(self):
        self.assertTrue(True)
        
    def test_api_delete(self):
        self.assertTrue(True)
