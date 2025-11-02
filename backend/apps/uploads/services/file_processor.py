# -*- coding: utf-8 -*-
"""
File Processor Service

CSV 파일 업로드 전체 프로세스를 오케스트레이션합니다.
"""
import os
import tempfile
from typing import Optional, Tuple, List, Dict
from django.db import transaction
from django.core.files.uploadedfile import UploadedFile

from apps.uploads.services.parsers import (
    DepartmentKPIParser,
    PublicationParser,
    ResearchProjectParser,
    StudentRosterParser
)
from apps.uploads.services.data_validator import DataValidator
from apps.dashboard.repositories.department_kpi_repository import DepartmentKPIRepository
from apps.dashboard.repositories.publication_repository import PublicationRepository
from apps.dashboard.repositories.research_project_repository import ResearchProjectRepository
from apps.dashboard.repositories.student_repository import StudentRepository


class FileProcessorService:
    """
    CSV 파일 처리 서비스

    파일 저장, 파싱, 검증, DB 저장을 담당합니다.
    """

    # 데이터 타입별 파서 매핑
    PARSER_MAP = {
        'department_kpi': DepartmentKPIParser,
        'publication': PublicationParser,
        'research_project': ResearchProjectParser,
        'student_roster': StudentRosterParser
    }

    # 데이터 타입별 Repository 매핑
    REPOSITORY_MAP = {
        'department_kpi': DepartmentKPIRepository,
        'publication': PublicationRepository,
        'research_project': ResearchProjectRepository,
        'student_roster': StudentRepository
    }

    # 데이터 타입별 Validator 메서드 매핑
    VALIDATOR_MAP = {
        'department_kpi': DataValidator.validate_department_kpi,
        'publication': DataValidator.validate_publication,
        'research_project': DataValidator.validate_research_project,
        'student_roster': DataValidator.validate_student_roster
    }

    @transaction.atomic
    def process_file(
        self, file: UploadedFile, data_type: str
    ) -> Dict:
        """
        CSV 파일 업로드 전체 프로세스

        Args:
            file: 업로드된 파일
            data_type: 데이터 유형
                ('department_kpi', 'publication', 'research_project', 'student_roster')

        Returns:
            Dict: 업로드 결과
                {
                    'success': bool,
                    'filename': str,
                    'data_type': str,
                    'rows_processed': int,
                    'errors': List[str] (optional)
                }

        Raises:
            ValueError: 데이터 타입 또는 파일 형식 오류
        """
        temp_file_path: Optional[str] = None

        try:
            # 1. 데이터 타입 검증
            if data_type not in self.PARSER_MAP:
                raise ValueError(
                    f"지원하지 않는 데이터 유형입니다: {data_type}. "
                    f"허용된 값: {', '.join(self.PARSER_MAP.keys())}"
                )

            # 2. 파일 확장자 검증 (.csv만 허용)
            if not file.name.lower().endswith('.csv'):
                raise ValueError("CSV 파일만 업로드 가능합니다")

            # 3. 임시 파일 저장
            temp_file_path = self._save_temp_file(file)

            # 4. 파일 파싱
            parser_class = self.PARSER_MAP[data_type]
            parsed_data = parser_class.parse(temp_file_path)

            # 5. 데이터 검증
            validator_func = self.VALIDATOR_MAP[data_type]
            is_valid, errors = validator_func(parsed_data)

            if not is_valid:
                return {
                    'success': False,
                    'filename': file.name,
                    'data_type': data_type,
                    'rows_processed': 0,
                    'errors': errors
                }

            # 6. 데이터 저장
            repository = self.REPOSITORY_MAP[data_type]
            rows_processed = repository.bulk_create(parsed_data)

            # 7. 성공 결과 반환
            return {
                'success': True,
                'filename': file.name,
                'data_type': data_type,
                'rows_processed': rows_processed
            }

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
        except Exception:
            pass  # 임시 파일 삭제 실패는 무시
