# -*- coding: utf-8 -*-
"""
Dashboard Domain 모델

순수 비즈니스 엔티티 정의 (프레임워크 독립적)
실제 CSV 데이터 타입과 대시보드 요구사항에 맞춰 작성
"""
from dataclasses import dataclass
from decimal import Decimal
from datetime import date
from typing import Optional, List, Dict, Any, Literal


# ==================== 데이터 엔티티 (4가지 CSV 타입) ====================

@dataclass
class DepartmentKPI:
    """
    학과 KPI 데이터 도메인 모델

    CSV: department_kpi.csv

    Attributes:
        id: 고유 ID
        evaluation_year: 평가년도
        college: 단과대학
        department: 학과
        employment_rate: 졸업생 취업률 (%)
        full_time_faculty: 전임교원 수 (명)
        visiting_faculty: 초빙교원 수 (명)
        tech_transfer_income: 기술이전 수입액 (억원)
        intl_conferences: 국제학술대회 개최 횟수
    """
    id: int
    evaluation_year: int
    college: str
    department: str
    employment_rate: Decimal
    full_time_faculty: int
    visiting_faculty: int
    tech_transfer_income: Decimal
    intl_conferences: int


@dataclass
class Publication:
    """
    논문 목록 도메인 모델

    CSV: publication_list.csv

    Attributes:
        id: 고유 ID
        paper_id: 논문 ID (PUB-YY-NNN)
        publication_date: 게재일
        college: 단과대학
        department: 학과
        paper_title: 논문 제목
        lead_author: 주저자
        co_authors: 참여저자 (세미콜론 구분)
        journal_name: 학술지명
        journal_grade: 저널 등급 (SCIE/KCI)
        impact_factor: Impact Factor
        project_linked: 과제연계여부 (Y/N)
    """
    id: int
    paper_id: str
    publication_date: date
    college: str
    department: str
    paper_title: str
    lead_author: str
    co_authors: Optional[str]
    journal_name: str
    journal_grade: Literal['SCIE', 'KCI']
    impact_factor: Optional[Decimal]
    project_linked: Literal['Y', 'N']


# 하위 호환성을 위한 별칭
Paper = Publication


@dataclass
class PaperCount:
    """
    논문 수 집계

    Attributes:
        count: 논문 수
        department: 학과명 (Optional)
    """
    count: int
    department: Optional[str] = None


@dataclass
class ResearchProject:
    """
    연구 과제 데이터 도메인 모델

    CSV: research_project_data.csv

    Attributes:
        id: 고유 ID
        execution_id: 집행 ID (T2324NNN)
        project_number: 과제번호
        project_name: 과제명
        principal_investigator: 연구책임자
        department: 소속학과
        funding_agency: 지원기관
        total_budget: 총 연구비 (원)
        execution_date: 집행일자
        execution_item: 집행 항목
        execution_amount: 집행 금액 (원)
        status: 상태 (집행완료/처리중)
        remarks: 비고
    """
    id: int
    execution_id: str
    project_number: str
    project_name: str
    principal_investigator: str
    department: str
    funding_agency: str
    total_budget: int
    execution_date: date
    execution_item: str
    execution_amount: int
    status: Literal['집행완료', '처리중']
    remarks: Optional[str]


@dataclass
class Student:
    """
    학생 명단 도메인 모델

    CSV: student_roster.csv

    Attributes:
        id: 고유 ID
        student_id: 학번 (YYYYMMNNN)
        name: 이름
        college: 단과대학
        department: 학과
        grade: 학년 (0~4)
        program_type: 과정 구분 (학사/석사/박사)
        enrollment_status: 학적 상태 (재학/휴학/졸업)
        gender: 성별 (남/여)
        admission_year: 입학년도
        advisor: 지도교수
        email: 이메일
    """
    id: int
    student_id: str
    name: str
    college: str
    department: str
    grade: int
    program_type: Literal['학사', '석사', '박사']
    enrollment_status: Literal['재학', '휴학', '졸업']
    gender: Literal['남', '여']
    admission_year: int
    advisor: Optional[str]
    email: str


# ==================== 실적 데이터 모델 (Performance - 레거시) ====================

@dataclass
class Performance:
    """
    실적 데이터 도메인 모델 (레거시)

    Attributes:
        id: 고유 ID
        date: 실적 날짜
        amount: 실적 금액
        category: 실적 분류
        department: 부서명
    """
    id: int
    date: date
    amount: Decimal
    category: Optional[str]
    department: Optional[str]


@dataclass
class PerformanceSummary:
    """
    실적 요약 데이터

    Attributes:
        total_amount: 총 금액
        count: 실적 건수
        year: 연도
    """
    total_amount: Decimal
    count: int
    year: int


# ==================== 대시보드 집계 모델 ====================

@dataclass
class KPISummary:
    """
    학과 KPI 요약 데이터

    대시보드 메인 화면에 표시될 집계 데이터

    Attributes:
        avg_employment_rate: 평균 취업률 (%)
        total_full_time_faculty: 전임교원 총 인원
        total_visiting_faculty: 초빙교원 총 인원
        total_tech_transfer_income: 기술이전 수입 총액 (억원)
        total_intl_conferences: 국제학술대회 개최 총 횟수
        by_college: 단과대학별 집계 목록
    """
    avg_employment_rate: Decimal
    total_full_time_faculty: int
    total_visiting_faculty: int
    total_tech_transfer_income: Decimal
    total_intl_conferences: int
    by_college: List['KPIByCollege']


@dataclass
class KPIByCollege:
    """
    단과대학별 KPI 집계

    Attributes:
        college: 단과대학명
        avg_employment_rate: 평균 취업률
        total_faculty: 총 교원 수 (전임 + 초빙)
    """
    college: str
    avg_employment_rate: Decimal
    total_faculty: int


@dataclass
class PublicationStats:
    """
    논문 통계

    Attributes:
        total_papers: 총 논문 수
        scie_count: SCIE 논문 수
        kci_count: KCI 논문 수
        avg_impact_factor: 평균 Impact Factor (SCIE만)
        project_linked_ratio: 과제 연계 논문 비율
        by_department: 학과별 논문 수
    """
    total_papers: int
    scie_count: int
    kci_count: int
    avg_impact_factor: Decimal
    project_linked_ratio: Decimal
    by_department: List['PublicationByDepartment']


@dataclass
class PublicationByDepartment:
    """
    학과별 논문 수

    Attributes:
        department: 학과명
        count: 논문 수
    """
    department: str
    count: int


@dataclass
class BudgetSummary:
    """
    예산 요약

    Attributes:
        total_budget: 총 연구비
        total_execution: 총 집행액
        execution_rate: 집행률 (0~1)
        by_item: 집행 항목별 집계
        by_agency: 지원 기관별 집계
    """
    total_budget: int
    total_execution: int
    execution_rate: Decimal
    by_item: List['BudgetByItem']
    by_agency: List['BudgetByAgency']


@dataclass
class BudgetByItem:
    """
    집행 항목별 집계

    Attributes:
        execution_item: 집행 항목명
        total_amount: 총 집행액
    """
    execution_item: str
    total_amount: int


@dataclass
class BudgetByAgency:
    """
    지원 기관별 집계

    Attributes:
        funding_agency: 지원 기관명
        total_budget: 총 연구비
    """
    funding_agency: str
    total_budget: int


@dataclass
class StudentStats:
    """
    학생 통계

    Attributes:
        total_students: 총 학생 수
        by_program: 과정별 학생 수
        by_status: 학적 상태별 학생 수
        by_department: 학과별 학생 수
    """
    total_students: int
    by_program: List['StudentByProgram']
    by_status: List['StudentByStatus']
    by_department: List['StudentByDepartment']


@dataclass
class StudentByProgram:
    """
    과정별 학생 수

    Attributes:
        program_type: 과정 구분 (학사/석사/박사)
        count: 학생 수
    """
    program_type: str
    count: int


@dataclass
class StudentByStatus:
    """
    학적 상태별 학생 수

    Attributes:
        enrollment_status: 학적 상태 (재학/휴학/졸업)
        count: 학생 수
    """
    enrollment_status: str
    count: int


@dataclass
class StudentByDepartment:
    """
    학과별 학생 수

    Attributes:
        department: 학과명
        count: 학생 수
    """
    department: str
    count: int


# ==================== 대시보드 전체 모델 ====================

@dataclass
class DashboardSummary:
    """
    대시보드 전체 요약 데이터

    /api/dashboard/ API 응답 모델

    Attributes:
        kpi_summary: 학과 KPI 요약
        publication_stats: 논문 통계
        student_stats: 학생 통계
        budget_summary: 예산 요약
    """
    kpi_summary: KPISummary
    publication_stats: PublicationStats
    student_stats: StudentStats
    budget_summary: BudgetSummary


# ==================== KPI 지표 모델 ====================

@dataclass
class KPIMetric:
    """
    핵심 성과 지표 메트릭

    대시보드 KPI 카드에 표시될 데이터

    Attributes:
        value: 지표 값
        unit: 단위 (%, 명, 억원 등)
        change_rate: 전년 대비 증감률 (%)
        trend: 추세 방향 (up/down/neutral)
    """
    value: Decimal
    unit: str
    change_rate: Decimal
    trend: Literal['up', 'down', 'neutral']


# KPI 별칭 (하위 호환성)
KPI = KPIMetric


@dataclass
class DashboardData:
    """
    대시보드 전체 데이터 (서비스 레이어용)

    Attributes:
        kpis: KPI 지표들
        charts: 차트 데이터
        filters: 필터 정보
    """
    kpis: Dict[str, KPIMetric]
    charts: Dict[str, List[Dict[str, Any]]]
    filters: Dict[str, Any]
