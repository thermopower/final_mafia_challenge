# -*- coding: utf-8 -*-
"""
Uploads Persistence 모델

CSV 파일 업로드 이력 추적 모델
"""
from django.db import models
from django.core.validators import MinValueValidator


class UploadHistory(models.Model):
    """
    업로드 이력 ORM 모델

    CSV 파일 업로드 추적

    Attributes:
        file_name: 파일명
        data_type: 데이터 유형 (4가지 CSV 타입 중 하나)
        rows_processed: 성공적으로 처리된 행 수
        status: 업로드 상태 (success/partial/failed)
        error_message: 오류 발생 시 상세 메시지
        uploaded_by: 업로드한 사용자
        uploaded_at: 업로드 시각
    """
    file_name = models.CharField(
        max_length=255,
        verbose_name="파일명"
    )
    data_type = models.CharField(
        max_length=50,
        choices=[
            ('department_kpi', '학과 KPI 데이터'),
            ('publication', '논문 목록'),
            ('research_project', '연구 과제 데이터'),
            ('student_roster', '학생 명단'),
        ],
        verbose_name="데이터 유형"
    )
    rows_processed = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="처리된 행 수"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', '전체 성공'),
            ('partial', '부분 성공'),
            ('failed', '전체 실패'),
        ],
        verbose_name="업로드 상태"
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name="오류 메시지"
    )
    uploaded_by = models.CharField(
        max_length=100,
        verbose_name="업로드 사용자"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="업로드 일시"
    )

    class Meta:
        db_table = 'upload_history'
        verbose_name = '업로드 이력'
        verbose_name_plural = '업로드 이력 목록'
        indexes = [
            models.Index(fields=['uploaded_at'], name='idx_upload_history_date'),
            models.Index(fields=['data_type'], name='idx_upload_history_type'),
            models.Index(fields=['status'], name='idx_upload_history_status'),
            models.Index(fields=['uploaded_by'], name='idx_upload_history_user'),
        ]
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.file_name} - {self.status} ({self.uploaded_at})"
