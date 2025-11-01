# -*- coding: utf-8 -*-
"""
CSV Export Service Tests
"""

import pytest
from decimal import Decimal
from datetime import date, datetime
from io import StringIO
import csv
from unittest.mock import Mock

from apps.data.services.csv_export_service import CSVExportService
from apps.data.domain.models import DataType, DataFilter, UnifiedDataItem


class TestCSVExportService:
    """CSVExportService 단위 테스트"""

    def test_generate_csv_headers_for_performance(self):
        """Performance 데이터 유형의 CSV 헤더 생성 테스트"""
        # Arrange
        service = CSVExportService()

        # Act
        headers = service._get_csv_headers(DataType.PERFORMANCE)

        # Assert
        assert headers == ["날짜", "항목", "금액", "카테고리", "설명"]

    def test_generate_csv_headers_for_paper(self):
        """Paper 데이터 유형의 CSV 헤더 생성 테스트"""
        # Arrange
        service = CSVExportService()

        # Act
        headers = service._get_csv_headers(DataType.PAPER)

        # Assert
        assert headers == ["게재일", "논문 제목", "저자", "학술지명", "분야", "DOI"]

    def test_generate_csv_headers_for_student(self):
        """Student 데이터 유형의 CSV 헤더 생성 테스트"""
        # Arrange
        service = CSVExportService()

        # Act
        headers = service._get_csv_headers(DataType.STUDENT)

        # Assert
        assert headers == ["학번", "이름", "학과", "학년", "상태"]

    def test_generate_csv_headers_for_budget(self):
        """Budget 데이터 유형의 CSV 헤더 생성 테스트"""
        # Arrange
        service = CSVExportService()

        # Act
        headers = service._get_csv_headers(DataType.BUDGET)

        # Assert
        assert headers == ["회계연도", "분기", "항목", "금액", "카테고리", "설명"]

    def test_convert_unified_item_to_csv_row_performance(self):
        """UnifiedDataItem을 CSV 행으로 변환 - Performance"""
        # Arrange
        service = CSVExportService()
        item = UnifiedDataItem(
            id=1,
            data_type=DataType.PERFORMANCE,
            date=date(2024, 1, 15),
            title="연구과제 A",
            uploaded_at=datetime(2024, 1, 15, 10, 30),
            uploaded_by="admin@example.com",
            amount=Decimal("1000000"),
            category="연구비",
            description="정부지원 연구과제"
        )

        # Act
        row = service._item_to_csv_row(item)

        # Assert
        assert row == ["2024-01-15", "연구과제 A", "1000000", "연구비", "정부지원 연구과제"]

    def test_convert_unified_item_to_csv_row_paper(self):
        """UnifiedDataItem을 CSV 행으로 변환 - Paper"""
        # Arrange
        service = CSVExportService()
        item = UnifiedDataItem(
            id=2,
            data_type=DataType.PAPER,
            date=date(2024, 2, 20),
            title="딥러닝 연구",
            uploaded_at=datetime(2024, 2, 20, 14, 0),
            uploaded_by="user@example.com",
            category="SCIE",
            description=None,
            extra_fields={
                "authors": "홍길동, 김철수",
                "journal_name": "IEEE Transactions",
                "doi": "10.1234/example"
            }
        )

        # Act
        row = service._item_to_csv_row(item)

        # Assert
        assert row == ["2024-02-20", "딥러닝 연구", "홍길동, 김철수", "IEEE Transactions", "SCIE", "10.1234/example"]

    def test_generate_csv_content_with_utf8_bom(self):
        """UTF-8 with BOM 인코딩으로 CSV 콘텐츠 생성"""
        # Arrange
        service = CSVExportService()
        items = [
            UnifiedDataItem(
                id=1,
                data_type=DataType.PERFORMANCE,
                date=date(2024, 1, 15),
                title="연구과제 A",
                uploaded_at=datetime(2024, 1, 15, 10, 30),
                uploaded_by="admin@example.com",
                amount=Decimal("1000000"),
                category="연구비",
                description="정부지원"
            )
        ]

        # Act
        csv_content = service._generate_csv_content(items, DataType.PERFORMANCE)

        # Assert
        assert csv_content.startswith('\ufeff')  # UTF-8 BOM
        assert '날짜' in csv_content
        assert '연구과제 A' in csv_content

    def test_generate_csv_content_handles_special_characters(self):
        """특수문자(쉼표, 따옴표, 줄바꿈) 처리 테스트"""
        # Arrange
        service = CSVExportService()
        items = [
            UnifiedDataItem(
                id=1,
                data_type=DataType.PERFORMANCE,
                date=date(2024, 1, 15),
                title='연구과제, "특수" 문자',
                uploaded_at=datetime(2024, 1, 15, 10, 30),
                uploaded_by="admin@example.com",
                amount=Decimal("1000000"),
                category="연구비",
                description="줄바꿈\n포함"
            )
        ]

        # Act
        csv_content = service._generate_csv_content(items, DataType.PERFORMANCE)

        # Assert
        # CSV 파싱 검증
        reader = csv.reader(StringIO(csv_content.lstrip('\ufeff')))
        rows = list(reader)
        assert len(rows) == 2  # 헤더 + 1개 행
        assert '연구과제, "특수" 문자' in rows[1][1]

    def test_generate_csv_content_empty_list(self):
        """빈 리스트로 CSV 생성 시 헤더만 포함"""
        # Arrange
        service = CSVExportService()
        items = []

        # Act
        csv_content = service._generate_csv_content(items, DataType.PERFORMANCE)

        # Assert
        reader = csv.reader(StringIO(csv_content.lstrip('\ufeff')))
        rows = list(reader)
        assert len(rows) == 1  # 헤더만
        assert rows[0] == ["날짜", "항목", "금액", "카테고리", "설명"]

    def test_export_to_csv_applies_filters(self):
        """export_to_csv가 필터를 적용하는지 테스트"""
        # Arrange
        service = CSVExportService()
        mock_repo = Mock()
        mock_repo.get_all_without_pagination.return_value = []
        service.data_repository = mock_repo

        filters = DataFilter(data_type=DataType.PERFORMANCE, year=2024)

        # Act
        csv_content = service.export_to_csv(filters)

        # Assert
        mock_repo.get_all_without_pagination.assert_called_once_with(filters)
        assert csv_content.startswith('\ufeff')

    def test_generate_filename_with_type_and_timestamp(self):
        """파일명 생성 테스트 (데이터 유형 + 타임스탬프)"""
        # Arrange
        service = CSVExportService()

        # Act
        filename = service.generate_filename(DataType.PERFORMANCE)

        # Assert
        assert filename.startswith("performance_")
        assert filename.endswith(".csv")
        # 타임스탬프 형식 확인 (YYYYMMDD_HHMMSS)
        assert len(filename.split('_')) >= 3
