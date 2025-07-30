from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count
from .models import Feature
from .simple_serializers import SimpleFeatureSerializer


class MinimalFeatureViewSet(viewsets.ModelViewSet):
    """Minimal ViewSet for testing schema generation."""

    queryset = Feature.objects.all()
    serializer_class = SimpleFeatureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Return features ordered by creation date."""
        return Feature.objects.select_related("author").order_by("-created_at")
