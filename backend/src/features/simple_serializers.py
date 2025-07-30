from rest_framework import serializers
from .models import Feature


class SimpleFeatureSerializer(serializers.ModelSerializer):
    """Simplified Feature serializer for testing."""

    class Meta:
        model = Feature
        fields = ["id", "title", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
