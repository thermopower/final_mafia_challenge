"""업로드 앱 설정"""
from django.apps import AppConfig


class UploadsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.uploads"
    verbose_name = "파일 업로드"
