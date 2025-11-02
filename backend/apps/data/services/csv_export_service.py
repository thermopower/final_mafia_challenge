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

    # 데이터 유형별 CSV 헤더 정의 (설계 문서 기준)
    HEADERS = {
        DataType.DEPARTMENT_KPI: [
            "평가년도", "단과대학", "학과", "취업률", "전임교원수", "초빙교원수", "기술이전수입", "학술대회개최"
        ],
        DataType.PUBLICATION: [
            "논문ID", "게재일", "단과대학", "학과", "논문제목", "주저자", "참여저자", "학술지명", "저널등급", "ImpactFactor", "과제연계"
        ],
        DataType.RESEARCH_PROJECT: [
            "집행ID", "과제번호", "과제명", "연구책임자", "소속학과", "지원기관", "총연구비", "집행일자", "집행항목", "집행금액", "상태", "비고"
        ],
        DataType.STUDENT_ROSTER: [
            "학번", "이름", "단과대학", "학과", "학년", "과정구분", "학적상태", "성별", "입학년도", "지도교수", "이메일"
        ],
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
            # 기본값: DEPARTMENT_KPI
            data_type = DataType.DEPARTMENT_KPI

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
        extra = item.extra_fields or {}

        if item.data_type == DataType.DEPARTMENT_KPI:
            # "평가년도", "단과대학", "학과", "취업률", "전임교원수", "초빙교원수", "기술이전수입", "학술대회개최"
            return [
                str(extra.get("evaluation_year", "")),
                item.category or "",  # college
                extra.get("department", ""),
                str(extra.get("employment_rate", "")),
                str(extra.get("full_time_faculty", "")),
                str(extra.get("visiting_faculty", "")),
                str(extra.get("tech_transfer_income", "")),
                str(extra.get("intl_conferences", "")),
            ]

        elif item.data_type == DataType.PUBLICATION:
            # "논문ID", "게재일", "단과대학", "학과", "논문제목", "주저자", "참여저자", "학술지명", "저널등급", "ImpactFactor", "과제연계"
            return [
                extra.get("paper_id", ""),
                item.date.isoformat() if item.date else "",
                extra.get("college", ""),
                item.category or "",  # department
                item.title or "",  # paper_title
                extra.get("lead_author", ""),
                extra.get("co_authors", ""),
                extra.get("journal_name", ""),
                extra.get("journal_grade", ""),
                str(extra.get("impact_factor", "")) if extra.get("impact_factor") is not None else "",
                extra.get("project_linked", ""),
            ]

        elif item.data_type == DataType.RESEARCH_PROJECT:
            # "집행ID", "과제번호", "과제명", "연구책임자", "소속학과", "지원기관", "총연구비", "집행일자", "집행항목", "집행금액", "상태", "비고"
            return [
                extra.get("execution_id", ""),
                extra.get("project_number", ""),
                item.title or "",  # project_name
                extra.get("principal_investigator", ""),
                item.category or "",  # department
                extra.get("funding_agency", ""),
                str(extra.get("total_budget", "")),
                item.date.isoformat() if item.date else "",  # execution_date
                extra.get("execution_item", ""),
                str(extra.get("execution_amount", "")),
                extra.get("status", ""),
                item.description or "",  # remarks
            ]

        elif item.data_type == DataType.STUDENT_ROSTER:
            # "학번", "이름", "단과대학", "학과", "학년", "과정구분", "학적상태", "성별", "입학년도", "지도교수", "이메일"
            return [
                extra.get("student_id", ""),
                item.title or "",  # name
                extra.get("college", ""),
                item.category or "",  # department
                str(extra.get("grade", "")),
                extra.get("program_type", ""),
                extra.get("enrollment_status", ""),
                extra.get("gender", ""),
                str(extra.get("admission_year", "")),
                extra.get("advisor", ""),
                extra.get("email", ""),
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
