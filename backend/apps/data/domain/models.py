# -*- coding: utf-8 -*-
"""
Data Domain Models

비즈니스 로직에서 사용되는 순수 도메인 모델입니다.
ORM 모델과 독립적으로 정의됩니다.
"""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from enum import Enum


class DataType(str, Enum):
    """
    데이터 유형 Enum

    4가지 CSV 타입과 매핑:
    - department_kpi: 학과 KPI 데이터
    - publication: 논문 목록
    - research_project: 연구 과제 데이터
    - student_roster: 학생 명단
    """
    DEPARTMENT_KPI = "department_kpi"
    PUBLICATION = "publication"
    RESEARCH_PROJECT = "research_project"
    STUDENT_ROSTER = "student_roster"


@dataclass
class PaginatedDataResult:
    """페이지네이션 결과를 담는 도메인 모델"""
    count: int  # 전체 결과 수
    next: Optional[str]  # 다음 페이지 URL
    previous: Optional[str]  # 이전 페이지 URL
    results: List[Dict[str, Any]]  # 결과 데이터 리스트


@dataclass
class DataFilter:
    """데이터 필터링 조건을 담는 도메인 모델"""
    data_type: Optional[DataType] = None  # 데이터 유형
    year: Optional[int] = None  # 연도
    search: Optional[str] = None  # 검색어
    ordering: str = "-date"  # 정렬 (기본값: 날짜 내림차순)


@dataclass
class UnifiedDataItem:
    """
    통합 데이터 항목 (모든 데이터 유형을 통합하여 표현)

    각 데이터 유형(performance, paper, student, budget)을
    공통 인터페이스로 표현합니다.
    """
    id: int
    data_type: DataType  # 데이터 유형
    date: date  # 날짜 (performance/paper의 경우)
    title: str  # 제목/항목명
    uploaded_at: datetime  # 업로드 일시
    uploaded_by: str  # 업로드 사용자 이메일
    amount: Optional[Decimal] = None  # 금액 (performance/budget)
    category: Optional[str] = None  # 카테고리
    description: Optional[str] = None  # 설명
    # 각 데이터 유형별 추가 필드 (Optional)
    extra_fields: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        base_dict = {
            "id": self.id,
            "type": self.data_type.value,
            "date": self.date.isoformat() if isinstance(self.date, date) else str(self.date),
            "title": self.title,
            "amount": float(self.amount) if self.amount else None,
            "category": self.category,
            "description": self.description,
            "uploaded_at": self.uploaded_at.isoformat() if isinstance(self.uploaded_at, datetime) else str(self.uploaded_at),
            "uploaded_by": self.uploaded_by,
        }

        # extra_fields가 있으면 병합
        if self.extra_fields:
            base_dict.update(self.extra_fields)

        return base_dict
