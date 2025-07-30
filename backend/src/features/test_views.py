from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Test endpoint",
    description="Simple test endpoint to verify schema generation",
    responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}},
)
@api_view(["GET"])
def test_endpoint(request):
    """Simple test endpoint."""
    return Response({"message": "Schema generation test successful"})
