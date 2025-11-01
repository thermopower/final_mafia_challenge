# -*- coding: utf-8 -*-
"""
CSVExportService

데이터를 CSV 파일로 내보내는 비즈니스 로직을 담당합니다.
"""

import csv
from io import StringIO
from typing import List, Optional
from datetime import datetime

from apps.data.domain.models import DataType, DataFilter, UnifiedDataItem
from apps.data.repositories.data_repository import DataRepository


class CSVExportService:
    """
    CSV 내보내기 서비스

    Responsibility:
    - 필터링된 데이터를 CSV 형식으로 변환
    - UTF-8 with BOM 인코딩 적용
    - 데이터 유형별 컬럼 헤더 정의
    """

    # 데이터 유형별 CSV 헤더 정의
    HEADERS = {
        DataType.PERFORMANCE: ["날짜", "항목", "금액", "카테고리", "설명"],
        DataType.PAPER: ["게재일", "논문 제목", "저자", "학술지명", "분야", "DOI"],
        DataType.STUDENT: ["학번", "이름", "학과", "학년", "상태"],
        DataType.BUDGET: ["회계연도", "분기", "항목", "금액", "카테고리", "설명"],
    }

    def __init__(self, data_repository: Optional[DataRepository] = None):
        """
        Args:
            data_repository: DataRepository 인스턴스 (의존성 주입)
        """
        self.data_repository = data_repository or DataRepository()

    def export_to_csv(self, filters: DataFilter) -> str:
        """
        필터 조건에 맞는 데이터를 CSV 문자열로 변환

        Args:
            filters: 필터 조건

        Returns:
            UTF-8 with BOM으로 인코딩된 CSV 문자열
        """
        # 1. 필터링된 모든 데이터 조회 (페이지네이션 없음)
        items = self.data_repository.get_all_without_pagination(filters)

        # 2. 데이터 유형 결정 (필터에서 단일 유형 또는 첫 번째 항목에서 추출)
        if filters.data_type:
            data_type = filters.data_type
        elif items:
            data_type = items[0].data_type
        else:
            # 기본값: PERFORMANCE
            data_type = DataType.PERFORMANCE

        # 3. CSV 생성
        return self._generate_csv_content(items, data_type)

    def generate_filename(self, data_type: DataType) -> str:
        """
        CSV 파일명 생성

        Args:
            data_type: 데이터 유형

        Returns:
            파일명 (예: "performance_20241101_103000.csv")
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{data_type.value}_{timestamp}.csv"

    def _get_csv_headers(self, data_type: DataType) -> List[str]:
        """
        데이터 유형별 CSV 헤더 반환

        Args:
            data_type: 데이터 유형

        Returns:
            헤더 리스트
        """
        return self.HEADERS.get(data_type, [])

    def _item_to_csv_row(self, item: UnifiedDataItem) -> List[str]:
        """
        UnifiedDataItem을 CSV 행으로 변환

        Args:
            item: 통합 데이터 항목

        Returns:
            CSV 행 (리스트)
        """
        if item.data_type == DataType.PERFORMANCE:
            return [
                item.date.isoformat() if item.date else "",
                item.title or "",
                str(item.amount) if item.amount else "",
                item.category or "",
                item.description or "",
            ]

        elif item.data_type == DataType.PAPER:
            extra = item.extra_fields or {}
            return [
                item.date.isoformat() if item.date else "",
                item.title or "",
                extra.get("authors", ""),
                extra.get("journal_name", ""),
                item.category or "",
                extra.get("doi", ""),
            ]

        elif item.data_type == DataType.STUDENT:
            extra = item.extra_fields or {}
            return [
                extra.get("student_id", ""),
                item.title or "",  # name
                item.category or "",  # department
                str(extra.get("grade", "")),
                extra.get("status", ""),
            ]

        elif item.data_type == DataType.BUDGET:
            extra = item.extra_fields or {}
            return [
                str(extra.get("fiscal_year", "")),
                str(extra.get("quarter", "")) if extra.get("quarter") else "",
                item.title or "",
                str(item.amount) if item.amount else "",
                item.category or "",
                item.description or "",
            ]

        else:
            return []

    def _generate_csv_content(self, items: List[UnifiedDataItem], data_type: DataType) -> str:
        """
        CSV 콘텐츠 생성 (UTF-8 with BOM)

        Args:
            items: 데이터 항목 리스트
            data_type: 데이터 유형

        Returns:
            UTF-8 with BOM으로 인코딩된 CSV 문자열
        """
        output = StringIO()
        # UTF-8 BOM 추가
        output.write('\ufeff')

        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

        # 헤더 작성
        headers = self._get_csv_headers(data_type)
        writer.writerow(headers)

        # 데이터 행 작성
        for item in items:
            row = self._item_to_csv_row(item)
            writer.writerow(row)

        return output.getvalue()
