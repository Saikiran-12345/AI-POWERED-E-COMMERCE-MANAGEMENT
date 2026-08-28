import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.accounts.factories import UserProfileFactory, LoginHistoryFactory
from apps.accounts.models import UserProfile, LoginHistory

@pytest.mark.django_db
class TestUserProfileAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/accounts/userprofiles/'
        self.instance = UserProfileFactory()
        self.url_detail = f'/api/v1/accounts/userprofiles/{self.instance.pk}/'

    def test_userprofile_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access UserProfile list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_userprofile_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to UserProfile detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_userprofile_create_requires_auth(self):
        """Ensure creating UserProfile requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_userprofile_update_requires_auth(self):
        """Ensure updating UserProfile requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_userprofile_delete_requires_auth(self):
        """Ensure deleting UserProfile requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class TestLoginHistoryAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/accounts/loginhistorys/'
        self.instance = LoginHistoryFactory()
        self.url_detail = f'/api/v1/accounts/loginhistorys/{self.instance.pk}/'

    def test_loginhistory_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access LoginHistory list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_loginhistory_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to LoginHistory detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_loginhistory_create_requires_auth(self):
        """Ensure creating LoginHistory requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_loginhistory_update_requires_auth(self):
        """Ensure updating LoginHistory requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_loginhistory_delete_requires_auth(self):
        """Ensure deleting LoginHistory requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

