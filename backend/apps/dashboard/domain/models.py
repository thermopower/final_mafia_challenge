# -*- coding: utf-8 -*-
"""
Dashboard Domain 모델

순수 비즈니스 엔티티 정의 (프레임워크 독립적)
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict, Any, Literal


@dataclass
class KPI:
    """
    핵심 성과 지표 (Key Performance Indicator)

    Attributes:
        value: 지표 값
        unit: 단위 (억원, 편, 명, %)
        change_rate: 전년 대비 증감률 (%)
        trend: 추세 (up, down, neutral)
    """
    value: Decimal
    unit: str
    change_rate: Decimal
    trend: Literal['up', 'down', 'neutral']


@dataclass
class DashboardData:
    """
    대시보드 전체 데이터

    Attributes:
        kpis: KPI 딕셔너리 (performance, papers, students, budget)
        charts: 차트 데이터 딕셔너리
        filters: 필터 조건 딕셔너리
    """
    kpis: Dict[str, KPI]
    charts: Dict[str, List[Dict[str, Any]]]
    filters: Dict[str, Any]


@dataclass
class PerformanceSummary:
    """
    실적 요약

    Attributes:
        total_amount: 총 금액
        count: 건수
        year: 연도
    """
    total_amount: Decimal
    count: int
    year: int


@dataclass
class PaperCount:
    """
    논문 집계

    Attributes:
        category: 카테고리 (SCI, KCI, 기타)
        count: 논문 수
    """
    category: str
    count: int


@dataclass
class StudentCount:
    """
    학생 집계

    Attributes:
        department: 학과
        count: 학생 수
    """
    department: str
    count: int


@dataclass
class BudgetRatio:
    """
    예산 비율

    Attributes:
        category: 카테고리 (인건비, 연구비, 운영비)
        amount: 금액
        percentage: 비율 (%)
    """
    category: str
    amount: Decimal
    percentage: Decimal


@dataclass
class Performance:
    """
    실적 도메인 모델

    Attributes:
        id: ID
        year: 연도
        month: 월
        department: 부서
        amount: 금액
        category: 카테고리
    """
    id: int
    year: int
    month: int
    department: str
    amount: Decimal
    category: str


@dataclass
class Paper:
    """
    논문 도메인 모델

    Attributes:
        id: ID
        category: 카테고리
    """
    id: int
    category: str


@dataclass
class Student:
    """
    학생 도메인 모델

    Attributes:
        id: ID
        department: 학과
    """
    id: int
    department: str


@dataclass
class Budget:
    """
    예산 도메인 모델

    Attributes:
        id: ID
        category: 카테고리
        amount: 금액
    """
    id: int
    category: str
    amount: Decimal
