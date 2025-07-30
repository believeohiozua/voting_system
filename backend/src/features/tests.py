from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Feature
import json


class FeatureModelTest(TestCase):
    def setUp(self):
        self.feature = Feature.objects.create(
            title="Test Feature", description="Test Description"
        )

    def test_feature_creation(self):
        """Test that a feature is created correctly"""
        self.assertEqual(self.feature.title, "Test Feature")
        self.assertEqual(self.feature.description, "Test Description")
        self.assertEqual(self.feature.votes, 0)
        self.assertIsNotNone(self.feature.id)
        self.assertIsNotNone(self.feature.created_at)

    def test_feature_string_representation(self):
        """Test the string representation of feature"""
        self.assertEqual(str(self.feature), "Test Feature")

    def test_feature_upvote(self):
        """Test the upvote functionality"""
        initial_votes = self.feature.votes
        self.feature.upvote()
        self.assertEqual(self.feature.votes, initial_votes + 1)

    def test_feature_ordering(self):
        """Test that features are ordered by votes then created_at"""
        feature2 = Feature.objects.create(title="Feature 2", votes=5)
        feature3 = Feature.objects.create(title="Feature 3", votes=10)

        features = Feature.objects.all()
        self.assertEqual(features[0], feature3)  # Highest votes first
        self.assertEqual(features[1], feature2)
        self.assertEqual(features[2], self.feature)  # Lowest votes last


class FeatureAPITest(APITestCase):
    def setUp(self):
        self.feature = Feature.objects.create(
            title="Test Feature", description="Test Description"
        )
        self.list_url = reverse("feature-list")
        self.detail_url = reverse("feature-detail", kwargs={"pk": self.feature.id})
        self.upvote_url = reverse("feature-upvote", kwargs={"pk": self.feature.id})

    def test_get_feature_list(self):
        """Test retrieving list of features"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Feature")

    def test_create_feature(self):
        """Test creating a new feature"""
        data = {"title": "New Feature", "description": "New Description"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feature.objects.count(), 2)
        self.assertEqual(response.data["title"], "New Feature")
        self.assertEqual(response.data["votes"], 0)

    def test_create_feature_without_title(self):
        """Test creating feature without title should fail"""
        data = {"description": "Description only"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_feature_without_description(self):
        """Test creating feature without description should work"""
        data = {"title": "Title only"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["description"], "")

    def test_upvote_feature(self):
        """Test upvoting a feature"""
        initial_votes = self.feature.votes
        response = self.client.post(self.upvote_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Feature upvoted successfully")

        # Refresh from database
        self.feature.refresh_from_db()
        self.assertEqual(self.feature.votes, initial_votes + 1)

    def test_upvote_nonexistent_feature(self):
        """Test upvoting a non-existent feature"""
        fake_url = reverse(
            "feature-upvote", kwargs={"pk": "00000000-0000-0000-0000-000000000000"}
        )
        response = self.client.post(fake_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_feature_detail(self):
        """Test retrieving a specific feature"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Feature")

    def test_features_ordered_by_votes(self):
        """Test that features are returned ordered by votes"""
        feature2 = Feature.objects.create(title="Popular Feature", votes=10)
        feature3 = Feature.objects.create(title="Very Popular Feature", votes=20)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should be ordered by votes descending
        self.assertEqual(response.data[0]["title"], "Very Popular Feature")
        self.assertEqual(response.data[1]["title"], "Popular Feature")
        self.assertEqual(response.data[2]["title"], "Test Feature")
