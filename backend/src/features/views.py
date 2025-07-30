from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models import Count
from .models import Feature
from .simple_serializers import SimpleFeatureSerializer as FeatureSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all features",
        description="Retrieve a list of all feature requests, ordered by votes (descending) and creation date.",
    ),
    create=extend_schema(
        summary="Create a new feature",
        description="Create a new feature request with title and optional description. Requires authentication.",
    ),
    retrieve=extend_schema(
        summary="Get a specific feature",
        description="Retrieve details of a specific feature by its ID.",
    ),
    update=extend_schema(
        summary="Update a feature",
        description="Update an existing feature's title and/or description. Only the author can update.",
    ),
    partial_update=extend_schema(
        summary="Partially update a feature",
        description="Partially update an existing feature's fields. Only the author can update.",
    ),
    destroy=extend_schema(
        summary="Delete a feature",
        description="Delete a feature request permanently. Only the author can delete.",
    ),
)
class FeatureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing feature requests.

    Provides CRUD operations for features and additional upvoting functionality.
    """

    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Return features ordered by vote count."""
        return (
            Feature.objects.select_related("author")
            .prefetch_related("votes")
            .annotate(vote_count=Count("votes"))
            .order_by("-vote_count", "-created_at")
        )

    def perform_create(self, serializer):
        """Set the author to the current user when creating a feature."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Only allow the author to update their feature."""
        if serializer.instance.author != self.request.user:
            raise PermissionError("You can only update your own features")
        serializer.save()

    def perform_destroy(self, instance):
        """Only allow the author to delete their feature."""
        if instance.author != self.request.user:
            raise PermissionError("You can only delete your own features")
        instance.delete()

    @extend_schema(
        summary="Upvote a feature",
        description="Add your vote to a feature. Requires authentication. You can only vote once per feature.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "vote_count": {"type": "integer"},
                    "has_voted": {"type": "boolean"},
                },
            },
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
            404: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def upvote(self, request, pk=None):
        """Upvote a feature request."""
        try:
            feature = self.get_object()

            # Check if user is trying to vote for their own feature
            if feature.author == request.user:
                return Response(
                    {"error": "You cannot vote for your own feature"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Try to add the vote
            vote_added = feature.upvote(request.user)

            if vote_added:
                return Response(
                    {
                        "message": "Feature upvoted successfully",
                        "vote_count": feature.vote_count,
                        "has_voted": True,
                    }
                )
            else:
                return Response(
                    {"error": "You have already voted for this feature"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Feature.DoesNotExist:
            return Response(
                {"error": "Feature not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="Remove vote from a feature",
        description="Remove your vote from a feature. Requires authentication.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "vote_count": {"type": "integer"},
                    "has_voted": {"type": "boolean"},
                },
            },
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
    )
    @action(detail=True, methods=["delete"], permission_classes=[IsAuthenticated])
    def remove_vote(self, request, pk=None):
        """Remove vote from a feature request."""
        try:
            feature = self.get_object()
            vote_removed = feature.remove_vote(request.user)

            if vote_removed:
                return Response(
                    {
                        "message": "Vote removed successfully",
                        "vote_count": feature.vote_count,
                        "has_voted": False,
                    }
                )
            else:
                return Response(
                    {"error": "You haven't voted for this feature"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Feature.DoesNotExist:
            return Response(
                {"error": "Feature not found"}, status=status.HTTP_404_NOT_FOUND
            )
