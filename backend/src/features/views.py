from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Feature
from .serializers import FeatureSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all features",
        description="Retrieve a list of all feature requests, ordered by votes (descending) and creation date.",
    ),
    create=extend_schema(
        summary="Create a new feature",
        description="Create a new feature request with title and optional description.",
    ),
    retrieve=extend_schema(
        summary="Get a specific feature",
        description="Retrieve details of a specific feature by its ID.",
    ),
    update=extend_schema(
        summary="Update a feature",
        description="Update an existing feature's title and/or description.",
    ),
    partial_update=extend_schema(
        summary="Partially update a feature",
        description="Partially update an existing feature's fields.",
    ),
    destroy=extend_schema(
        summary="Delete a feature",
        description="Delete a feature request permanently.",
    ),
)
class FeatureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing feature requests.

    Provides CRUD operations for features and additional upvoting functionality.
    """

    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    @extend_schema(
        summary="Upvote a feature",
        description="Increment the vote count for a specific feature by 1.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "votes": {"type": "integer"},
                },
            },
            404: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
    )
    @action(detail=True, methods=["post"])
    def upvote(self, request, pk=None):
        """Upvote a feature request."""
        try:
            feature = self.get_object()
            feature.upvote()
            return Response(
                {"message": "Feature upvoted successfully", "votes": feature.votes}
            )
        except Feature.DoesNotExist:
            return Response(
                {"error": "Feature not found"}, status=status.HTTP_404_NOT_FOUND
            )
