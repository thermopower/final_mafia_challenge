# -*- coding: utf-8 -*-
"""
File Processor Service

파일 업로드 전체 프로세스를 오케스트레이션합니다.
"""
import os
import tempfile
from typing import Optional
from django.db import transaction
from django.core.files.uploadedfile import UploadedFile

from apps.uploads.services.excel_parser import ExcelParser
from apps.uploads.services.data_validator import DataValidator
from apps.uploads.services.column_mapper import ColumnMapper
from apps.uploads.repositories.upload_repository import UploadRepository
from apps.dashboard.repositories.performance_repository import PerformanceRepository
from apps.dashboard.repositories.paper_repository import PaperRepository
from apps.dashboard.repositories.student_repository import StudentRepository
from apps.dashboard.repositories.budget_repository import BudgetRepository
from apps.uploads.domain.models import UploadResult, UploadRecord
from apps.core.exceptions import ValidationError
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class FileProcessorService:
    """
    파일 처리 서비스

    파일 저장, 파싱, 검증, DB 저장을 담당합니다.
    """

    def __init__(self):
        self.excel_parser = ExcelParser()
        self.data_validator = DataValidator()
        self.column_mapper = ColumnMapper()
        self.upload_repo = UploadRepository()
        self.performance_repo = PerformanceRepository()
        self.paper_repo = PaperRepository()
        self.student_repo = StudentRepository()
        self.budget_repo = BudgetRepository()

    @transaction.atomic
    def process_file(
        self, file: UploadedFile, data_type: str, user_id: str
    ) -> UploadResult:
        """
        파일 업로드 전체 프로세스

        Args:
            file: 업로드된 파일
            data_type: 데이터 유형 ('performance', 'paper', 'student', 'budget')
            user_id: 업로드한 사용자 ID

        Returns:
            UploadResult: 업로드 결과

        Raises:
            ValidationError: 검증 실패 시
        """
        temp_file_path: Optional[str] = None

        try:
            # 1. 임시 파일 저장
            temp_file_path = self._save_temp_file(file)

            # 2. 파일 파싱
            parsed_data = self.excel_parser.parse(temp_file_path)
            logger.info(
                f"Parsed {parsed_data.total_rows} rows from {file.name}"
            )

            # 3. 데이터 검증
            validation_result = self.data_validator.validate(
                parsed_data.rows, data_type
            )

            if not validation_result.is_valid:
                # 검증 실패 - 에러 정보와 함께 예외 발생
                error_details = {}

                if validation_result.missing_columns:
                    error_details["missing_columns"] = (
                        validation_result.missing_columns
                    )
                    error_details["current_columns"] = parsed_data.headers

                if validation_result.invalid_rows:
                    error_details["invalid_rows"] = (
                        validation_result.invalid_rows
                    )

                if validation_result.duplicates:
                    error_details["duplicates"] = validation_result.duplicates

                raise ValidationError(
                    message=self._get_validation_error_message(
                        validation_result
                    ),
                    error_code="VALIDATION_ERROR",
                    details=error_details,
                )

            # 4. 업로드 레코드 생성 (pending 상태)
            upload_record = self.upload_repo.create_upload_record(
                UploadRecord(
                    id=None,
                    filename=file.name,
                    data_type=data_type,
                    file_size=file.size,
                    rows_processed=0,
                    rows_failed=0,
                    status="processing",
                    error_message=None,
                    uploaded_by=user_id,
                    uploaded_at=None,
                    completed_at=None,
                )
            )

            # 5. 데이터 저장 (Repository에 따라 분기)
            rows_processed = self._save_data_to_db(
                parsed_data.rows, data_type, user_id
            )

            # 6. 업로드 레코드 상태 업데이트 (success)
            self.upload_repo.update_upload_status(
                upload_record.id, "success", rows_processed, 0
            )

            logger.info(
                f"Successfully processed {rows_processed} rows for {file.name}"
            )

            # 7. 업로드 결과 반환
            updated_record = self.upload_repo.get_by_id(upload_record.id)

            return UploadResult(
                success=True, upload_record=updated_record, errors=None
            )

        except ValidationError as e:
            # 검증 오류 - 그대로 재발생
            logger.warning(f"Validation error: {e.message}")
            raise

        except Exception as e:
            # 예상치 못한 오류
            logger.error(f"Unexpected error during file processing: {str(e)}")

            # 업로드 레코드가 생성되었다면 상태 업데이트
            if "upload_record" in locals():
                self.upload_repo.update_upload_status(
                    upload_record.id, "failed", 0, parsed_data.total_rows
                )

            raise ValidationError(
                message="업로드 중 오류가 발생했습니다",
                error_code="INTERNAL_ERROR",
                details={"error": str(e)},
            )

        finally:
            # 8. 임시 파일 삭제
            if temp_file_path:
                self._cleanup_temp_file(temp_file_path)

    def _save_temp_file(self, file: UploadedFile) -> str:
        """
        임시 파일 저장

        Args:
            file: 업로드된 파일

        Returns:
            str: 임시 파일 경로
        """
        # 임시 디렉토리에 저장
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file.name)

        with open(temp_file_path, "wb") as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        return temp_file_path

    def _cleanup_temp_file(self, file_path: str):
        """
        임시 파일 삭제

        Args:
            file_path: 파일 경로
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temp file: {str(e)}")

    def _save_data_to_db(
        self, data: list, data_type: str, user_id: str
    ) -> int:
        """
        데이터를 DB에 저장

        Args:
            data: 파싱된 데이터 리스트
            data_type: 데이터 유형
            user_id: 업로드한 사용자 ID

        Returns:
            int: 저장된 행 수
        """
        if data_type == "performance":
            return self.performance_repo.bulk_create(data, user_id)
        elif data_type == "paper":
            return self.paper_repo.bulk_create(data, user_id)
        elif data_type == "student":
            return self.student_repo.bulk_create(data, user_id)
        elif data_type == "budget":
            return self.budget_repo.bulk_create(data, user_id)
        else:
            raise ValidationError(
                message=f"지원하지 않는 데이터 유형입니다: {data_type}",
                error_code="INVALID_DATA_TYPE",
            )

    def _get_validation_error_message(self, validation_result) -> str:
        """
        검증 오류 메시지 생성

        Args:
            validation_result: 검증 결과

        Returns:
            str: 오류 메시지
        """
        if validation_result.missing_columns:
            return "필수 컬럼이 누락되었습니다"
        elif validation_result.invalid_rows:
            return "데이터 형식 오류"
        elif validation_result.duplicates:
            return "중복 데이터 발견"
        else:
            return "데이터 검증 실패"
