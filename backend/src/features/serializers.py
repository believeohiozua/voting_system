from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Feature


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for feature author information."""

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class FeatureSerializer(serializers.ModelSerializer):
    """Serializer for Feature model with user relationships."""

    id = serializers.UUIDField(
        read_only=True, help_text="Unique identifier for the feature"
    )
    title = serializers.CharField(max_length=200, help_text="Feature title (required)")
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional detailed description of the feature",
    )
    author = AuthorSerializer(read_only=True, help_text="User who created this feature")
    vote_count = serializers.IntegerField(
        read_only=True, help_text="Current number of votes"
    )
    has_voted = serializers.SerializerMethodField(
        help_text="Whether current user has voted"
    )
    created_at = serializers.DateTimeField(
        read_only=True, help_text="When the feature was created"
    )
    updated_at = serializers.DateTimeField(
        read_only=True, help_text="When the feature was last updated"
    )

    class Meta:
        model = Feature
        fields = [
            "id",
            "title",
            "description",
            "author",
            "vote_count",
            "has_voted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "author",
            "vote_count",
            "has_voted",
            "created_at",
            "updated_at",
        ]

    def get_has_voted(self, obj):
        """Check if the current user has voted for this feature."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.has_user_voted(request.user)
        return False

    def create(self, validated_data):
        """Create a new feature with the current user as author."""
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)
