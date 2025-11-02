# -*- coding: utf-8 -*-
"""
Upload Serializers

CSV 파일 업로드 요청/응답 직렬화
"""
from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    """
    CSV 파일 업로드 요청 Serializer
    """
    file = serializers.FileField(
        required=True,
        help_text="CSV 파일 (UTF-8 인코딩)"
    )
    data_type = serializers.ChoiceField(
        required=True,
        choices=[
            ('department_kpi', '학과 KPI 데이터'),
            ('publication', '논문 목록'),
            ('research_project', '연구 과제 데이터'),
            ('student_roster', '학생 명단')
        ],
        help_text="데이터 유형"
    )

    def validate_file(self, value):
        """
        파일 검증

        Args:
            value: 업로드된 파일

        Returns:
            업로드된 파일

        Raises:
            ValidationError: 파일 형식 또는 크기 오류
        """
        # 파일 확장자 검증
        if not value.name.lower().endswith('.csv'):
            raise serializers.ValidationError("CSV 파일만 업로드 가능합니다")

        # 파일 크기 검증 (최대 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError(
                f"파일 크기는 {max_size // (1024 * 1024)}MB 이하여야 합니다"
            )

        return value


class UploadResponseSerializer(serializers.Serializer):
    """
    CSV 파일 업로드 응답 Serializer
    """
    success = serializers.BooleanField(help_text="업로드 성공 여부")
    filename = serializers.CharField(help_text="파일명")
    data_type = serializers.CharField(help_text="데이터 유형")
    rows_processed = serializers.IntegerField(help_text="처리된 행 수")
    errors = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="오류 메시지 목록"
    )
