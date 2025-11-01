"""
업로드 ORM 모델

Django ORM 모델 정의
"""
from django.db import models
from apps.core.models import TimeStampedModel


class UploadedFile(TimeStampedModel):
    """업로드된 파일 메타데이터"""

    filename = models.CharField(max_length=255, verbose_name="파일명")
    data_type = models.CharField(
        max_length=50,
        choices=[
            ("performance", "실적"),
            ("paper", "논문"),
            ("student", "학생"),
            ("budget", "예산"),
        ],
        verbose_name="데이터 유형",
    )
    file_size = models.BigIntegerField(default=0, verbose_name="파일 크기 (bytes)")
    rows_processed = models.IntegerField(default=0, verbose_name="처리된 행 수")
    rows_failed = models.IntegerField(default=0, verbose_name="실패한 행 수")
    uploaded_by = models.CharField(max_length=255, verbose_name="업로드 사용자 이메일")
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "대기 중"),
            ("processing", "처리 중"),
            ("success", "성공"),
            ("failed", "실패"),
            ("partial", "부분 성공"),
        ],
        default="pending",
        verbose_name="상태",
    )
    error_message = models.TextField(blank=True, null=True, verbose_name="오류 메시지")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="완료 일시")

    class Meta:
        db_table = "uploaded_files"
        ordering = ["-created_at"]
        verbose_name = "업로드된 파일"
        verbose_name_plural = "업로드된 파일 목록"

    def __str__(self):
        return f"{self.filename} ({self.data_type})"
