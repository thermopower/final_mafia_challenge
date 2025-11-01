"""
Upload URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.uploads.presentation.views import ExcelUploadViewSet

router = DefaultRouter()
router.register(r"upload", ExcelUploadViewSet, basename="upload")

urlpatterns = [
    path("", include(router.urls)),
]
