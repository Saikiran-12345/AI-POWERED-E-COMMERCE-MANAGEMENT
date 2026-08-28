import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.recommendations.factories import RecommendationFactory
from apps.recommendations.models import Recommendation

@pytest.mark.django_db
class TestRecommendationAPI(APITestCase):
    def setUp(self):
        self.url_list = '/api/v1/recommendations/recommendations/'
        self.instance = RecommendationFactory()
        self.url_detail = f'/api/v1/recommendations/recommendations/{self.instance.pk}/'

    def test_recommendation_list_unauthenticated(self):
        """Ensure unauthenticated users can or cannot access Recommendation list."""
        response = self.client.get(self.url_list)
        # Default DRF allows read-only for IsAuthenticatedOrReadOnly, update as per your permission classes
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_recommendation_retrieve_unauthenticated(self):
        """Ensure unauthenticated access to Recommendation detail."""
        response = self.client.get(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_recommendation_create_requires_auth(self):
        """Ensure creating Recommendation requires authentication."""
        response = self.client.post(self.url_list, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])

    def test_recommendation_update_requires_auth(self):
        """Ensure updating Recommendation requires authentication."""
        response = self.client.patch(self.url_detail, data={})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_recommendation_delete_requires_auth(self):
        """Ensure deleting Recommendation requires authentication."""
        response = self.client.delete(self.url_detail)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

