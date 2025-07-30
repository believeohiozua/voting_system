from rest_framework import serializers
from .models import Feature


class FeatureSerializer(serializers.ModelSerializer):
    """Serializer for Feature model with detailed field descriptions."""

    id = serializers.UUIDField(
        read_only=True, help_text="Unique identifier for the feature"
    )
    title = serializers.CharField(max_length=200, help_text="Feature title (required)")
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional detailed description of the feature",
    )
    votes = serializers.IntegerField(
        read_only=True, help_text="Current number of votes"
    )
    created_at = serializers.DateTimeField(
        read_only=True, help_text="When the feature was created"
    )
    updated_at = serializers.DateTimeField(
        read_only=True, help_text="When the feature was last updated"
    )

    class Meta:
        model = Feature
        fields = ["id", "title", "description", "votes", "created_at", "updated_at"]
        read_only_fields = ["id", "votes", "created_at", "updated_at"]
