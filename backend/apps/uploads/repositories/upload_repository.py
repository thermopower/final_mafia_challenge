"""
업로드 Repository

업로드 파일 메타데이터 저장 및 조회
"""
from typing import Optional, List
from datetime import datetime
from apps.uploads.domain.models import UploadRecord
from apps.uploads.persistence.models import UploadedFile


class UploadRepository:
    """업로드 Repository"""

    def create_upload_record(self, upload_data: UploadRecord) -> UploadRecord:
        """
        업로드 이력 생성

        Args:
            upload_data: 업로드 도메인 모델

        Returns:
            생성된 업로드 레코드 (ID 포함)
        """
        orm_obj = UploadedFile.objects.create(
            filename=upload_data.filename,
            data_type=upload_data.data_type,
            file_size=upload_data.file_size,
            rows_processed=upload_data.rows_processed,
            rows_failed=upload_data.rows_failed,
            uploaded_by=upload_data.uploaded_by,
            status=upload_data.status,
            error_message=upload_data.error_message,
        )

        return self._to_domain(orm_obj)

    def get_upload_history(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[List[UploadRecord], int]:
        """
        업로드 이력 조회 (페이지네이션)

        Args:
            page: 페이지 번호 (1부터 시작)
            page_size: 페이지당 항목 수

        Returns:
            (upload_records, total_count) 튜플
        """
        offset = (page - 1) * page_size
        queryset = UploadedFile.objects.all()

        total_count = queryset.count()
        records = queryset[offset : offset + page_size]

        return [self._to_domain(record) for record in records], total_count

    def update_upload_status(
        self, upload_id: int, status: str, rows_processed: int, rows_failed: int = 0
    ) -> None:
        """
        업로드 상태 업데이트

        Args:
            upload_id: 업로드 ID
            status: 상태 ('success', 'failed', 'partial')
            rows_processed: 처리된 행 수
            rows_failed: 실패한 행 수
        """
        UploadedFile.objects.filter(id=upload_id).update(
            status=status,
            rows_processed=rows_processed,
            rows_failed=rows_failed,
            completed_at=datetime.now()
        )

    def get_by_id(self, upload_id: int) -> Optional[UploadRecord]:
        """
        업로드 레코드 조회 (ID로)

        Args:
            upload_id: 업로드 ID

        Returns:
            UploadRecord 또는 None
        """
        try:
            orm_obj = UploadedFile.objects.get(id=upload_id)
            return self._to_domain(orm_obj)
        except UploadedFile.DoesNotExist:
            return None

    def _to_domain(self, orm_obj: UploadedFile) -> UploadRecord:
        """ORM 모델 → 도메인 모델 변환"""
        return UploadRecord(
            id=orm_obj.id,
            filename=orm_obj.filename,
            data_type=orm_obj.data_type,
            file_size=orm_obj.file_size,
            rows_processed=orm_obj.rows_processed,
            rows_failed=orm_obj.rows_failed,
            uploaded_at=orm_obj.created_at,
            uploaded_by=orm_obj.uploaded_by,
            status=orm_obj.status,
            error_message=orm_obj.error_message,
            completed_at=orm_obj.completed_at,
        )
