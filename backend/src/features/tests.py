from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Feature, Vote


class FeatureModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.feature = Feature.objects.create(
            title="Test Feature", description="Test description", author=self.user
        )

    def test_feature_creation(self):
        """Test that a feature can be created."""
        self.assertEqual(self.feature.title, "Test Feature")
        self.assertEqual(self.feature.author, self.user)
        self.assertEqual(self.feature.vote_count, 0)

    def test_feature_upvote(self):
        """Test that a feature can be upvoted."""
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )

        # Test upvoting
        result = self.feature.upvote(other_user)
        self.assertTrue(result)  # Should return True for new vote
        self.assertEqual(self.feature.vote_count, 1)

        # Test duplicate upvote
        result = self.feature.upvote(other_user)
        self.assertFalse(result)  # Should return False for duplicate vote
        self.assertEqual(self.feature.vote_count, 1)

    def test_has_user_voted(self):
        """Test checking if user has voted."""
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )

        self.assertFalse(self.feature.has_user_voted(other_user))
        self.feature.upvote(other_user)
        self.assertTrue(self.feature.has_user_voted(other_user))


class FeatureAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.feature = Feature.objects.create(
            title="Test Feature", description="Test description", author=self.user
        )

    def test_list_features(self):
        """Test listing features."""
        url = reverse("feature-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_feature_authenticated(self):
        """Test creating a feature when authenticated."""
        self.client.force_authenticate(user=self.user)
        url = reverse("feature-list")
        data = {"title": "New Feature", "description": "New description"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feature.objects.count(), 2)

    def test_create_feature_unauthenticated(self):
        """Test creating a feature when not authenticated."""
        url = reverse("feature-list")
        data = {"title": "New Feature", "description": "New description"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upvote_feature(self):
        """Test upvoting a feature."""
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        self.client.force_authenticate(user=other_user)

        url = reverse("feature-upvote", kwargs={"pk": self.feature.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["vote_count"], 1)
        self.assertTrue(response.data["has_voted"])

    def test_upvote_own_feature(self):
        """Test that users cannot upvote their own features."""
        self.client.force_authenticate(user=self.user)

        url = reverse("feature-upvote", kwargs={"pk": self.feature.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cannot vote for your own feature", response.data["error"])


class SchemaTest(APITestCase):
    def test_schema_generation(self):
        """Test that the OpenAPI schema can be generated without errors."""
        url = reverse("schema")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("openapi", response.data)

    def test_swagger_ui(self):
        """Test that the Swagger UI loads without errors."""
        url = reverse("swagger-ui")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
