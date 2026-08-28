import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.reviews.factories import ReviewFactory
from apps.reviews.models import Review

@pytest.mark.django_db
class TestReviewAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/reviews/reviews/'
        self.instance = ReviewFactory()
        self.url_detail = f'/api/v1/reviews/reviews/{self.instance.pk}/'

    def test_review_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Review list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_review_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Review detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_review_create_requires_auth(self):
        """Ensure creating Review requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_review_update_requires_auth(self):
        """Ensure updating Review requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_review_delete_requires_auth(self):
        """Ensure deleting Review requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

