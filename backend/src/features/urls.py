from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .minimal_views import MinimalFeatureViewSet
from .test_views import test_endpoint

router = DefaultRouter()
router.register(r"features", MinimalFeatureViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/test/", test_endpoint, name="test-endpoint"),
]
