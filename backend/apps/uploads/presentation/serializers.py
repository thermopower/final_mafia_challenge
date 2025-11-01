"""
Upload Serializers
"""
from rest_framework import serializers
from apps.uploads.domain.models import UploadRecord


class ExcelUploadSerializer(serializers.Serializer):
    """Excel 업로드 Serializer"""

    file = serializers.FileField()
    data_type = serializers.ChoiceField(
        choices=["performance", "paper", "student", "budget"]
    )


class UploadRecordSerializer(serializers.Serializer):
    """업로드 레코드 Serializer"""

    id = serializers.IntegerField(read_only=True)
    filename = serializers.CharField(read_only=True)
    data_type = serializers.CharField(read_only=True)
    file_size = serializers.IntegerField(read_only=True)
    rows_processed = serializers.IntegerField(read_only=True)
    rows_failed = serializers.IntegerField(read_only=True)
    uploaded_at = serializers.DateTimeField(read_only=True)
    uploaded_by = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    error_message = serializers.CharField(read_only=True, allow_null=True)
    completed_at = serializers.DateTimeField(read_only=True, allow_null=True)
