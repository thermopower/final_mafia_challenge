# -*- coding: utf-8 -*-
"""
Dashboard Service

대시보드 비즈니스 로직
"""
from typing import Dict, List, Optional
from decimal import Decimal

from apps.dashboard.repositories.department_kpi_repository import DepartmentKPIRepository
from apps.dashboard.repositories.publication_repository import PublicationRepository
from apps.dashboard.repositories.student_repository import StudentRepository
from apps.dashboard.repositories.research_project_repository import ResearchProjectRepository
from apps.dashboard.services.metric_calculator import MetricCalculator
from apps.dashboard.services.chart_data_builder import ChartDataBuilder


class DashboardService:
    """
    대시보드 서비스

    4가지 데이터 소스를 통합하여 대시보드 데이터를 생성합니다.
    - 학과 KPI (DepartmentKPI)
    - 논문 (Publication)
    - 학생 (Student)
    - 연구 과제 (ResearchProject)
    """

    def __init__(
        self,
        dept_kpi_repo: DepartmentKPIRepository = None,
        publication_repo: PublicationRepository = None,
        student_repo: StudentRepository = None,
        research_project_repo: ResearchProjectRepository = None,
        metric_calculator: MetricCalculator = None,
        chart_builder: ChartDataBuilder = None
    ):
        self.dept_kpi_repo = dept_kpi_repo or DepartmentKPIRepository()
        self.publication_repo = publication_repo or PublicationRepository()
        self.student_repo = student_repo or StudentRepository()
        self.research_project_repo = research_project_repo or ResearchProjectRepository()
        self.metric_calculator = metric_calculator or MetricCalculator()
        self.chart_builder = chart_builder or ChartDataBuilder()

    def get_dashboard_data(self, year: int, college: Optional[str] = 'all') -> Dict:
        """
        대시보드 전체 데이터 조회 및 생성

        Args:
            year: 조회할 연도
            college: 단과대학 ('all'이면 전체)

        Returns:
            Dict: {
                'kpi_metrics': {...},  # 8개 KPI 메트릭
                'charts': {...}        # 9개 차트 데이터
            }
        """
        # 필터 조건 처리
        college_filter = None if college == 'all' else college

        # KPI 메트릭 생성
        kpi_metrics = self._build_kpi_metrics(year, college_filter)

        # 차트 데이터 생성
        charts = self._build_charts(year, college_filter)

        return {
            'kpi_metrics': kpi_metrics,
            'charts': charts
        }

    def _build_kpi_metrics(self, year: int, college: Optional[str]) -> Dict:
        """
        8개 KPI 메트릭 생성

        1. 전임교원 수
        2. 초빙교원 수
        3. 평균 취업률
        4. 기술이전 수입액
        5. 총 논문 수
        6. 평균 Impact Factor
        7. 총 학생 수
        8. 예산 집행률

        Args:
            year: 조회 연도
            college: 단과대학 (None이면 전체)

        Returns:
            Dict: {
                'full_time_faculty': {'value': 150, 'change_rate': 5.2},
                ...
            }
        """
        # 현재 연도 데이터
        current_kpi = self.dept_kpi_repo.get_summary(year, college)
        print(f"[DashboardService] current_kpi (year={year}, college={college}): {current_kpi}")

        current_pub = self.publication_repo.get_count_by_period(year)
        print(f"[DashboardService] current_pub (year={year}): {current_pub}")

        current_student = self.student_repo.get_stats('재학')
        print(f"[DashboardService] current_student: {current_student}")

        current_budget = self.research_project_repo.get_budget_stats()
        print(f"[DashboardService] current_budget: {current_budget}")

        # 이전 연도 데이터
        prev_year = year - 1
        prev_kpi = self.dept_kpi_repo.get_summary(prev_year, college)
        prev_pub = self.publication_repo.get_count_by_period(prev_year)
        prev_student = self.student_repo.get_stats('재학')
        # 예산 집행률은 연도 필터가 없으므로 임시로 현재 값 사용

        # 1. 전임교원 수
        full_time_faculty_value = current_kpi['total_full_time_faculty']
        full_time_faculty_change = self._safe_calculate_change_rate(
            Decimal(str(full_time_faculty_value)),
            Decimal(str(prev_kpi['total_full_time_faculty']))
        )

        # 2. 초빙교원 수
        visiting_faculty_value = current_kpi['total_visiting_faculty']
        visiting_faculty_change = self._safe_calculate_change_rate(
            Decimal(str(visiting_faculty_value)),
            Decimal(str(prev_kpi['total_visiting_faculty']))
        )

        # 3. 평균 취업률
        employment_rate_value = current_kpi['avg_employment_rate']
        employment_rate_change = self._safe_calculate_change_rate(
            employment_rate_value,
            prev_kpi['avg_employment_rate']
        )

        # 4. 기술이전 수입액
        tech_transfer_value = current_kpi['total_tech_transfer_income']
        tech_transfer_change = self._safe_calculate_change_rate(
            tech_transfer_value,
            prev_kpi['total_tech_transfer_income']
        )

        # 5. 총 논문 수
        total_papers_value = current_pub['total_papers']
        total_papers_change = self._safe_calculate_change_rate(
            Decimal(str(total_papers_value)),
            Decimal(str(prev_pub['total_papers']))
        )

        # 6. 평균 Impact Factor
        avg_if_value = current_pub['avg_impact_factor']
        avg_if_change = self._safe_calculate_change_rate(
            avg_if_value,
            prev_pub['avg_impact_factor']
        )

        # 7. 총 학생 수
        total_students_value = current_student['total_students']
        total_students_change = self._safe_calculate_change_rate(
            Decimal(str(total_students_value)),
            Decimal(str(prev_student['total_students']))
        )

        # 8. 예산 집행률
        budget_rate_value = current_budget['execution_rate']
        budget_rate_change = Decimal('0.0')  # 전년도 비교 불가 (필터 없음)

        return {
            'full_time_faculty': {
                'value': full_time_faculty_value,
                'change_rate': float(full_time_faculty_change)
            },
            'visiting_faculty': {
                'value': visiting_faculty_value,
                'change_rate': float(visiting_faculty_change)
            },
            'employment_rate': {
                'value': float(employment_rate_value),
                'change_rate': float(employment_rate_change)
            },
            'tech_transfer_income': {
                'value': float(tech_transfer_value),
                'change_rate': float(tech_transfer_change)
            },
            'total_papers': {
                'value': total_papers_value,
                'change_rate': float(total_papers_change)
            },
            'avg_impact_factor': {
                'value': float(avg_if_value),
                'change_rate': float(avg_if_change)
            },
            'total_students': {
                'value': total_students_value,
                'change_rate': float(total_students_change)
            },
            'budget_execution_rate': {
                'value': float(budget_rate_value),
                'change_rate': float(budget_rate_change)
            }
        }

    def _build_charts(self, year: int, college: Optional[str]) -> Dict:
        """
        9개 차트 데이터 생성

        1. 학과별 취업률 (막대)
        2. 연도별 교원 수 추이 (라인)
        3. 기술이전 수입액 추이 (라인)
        4. SCIE/KCI 논문 분포 (파이)
        5. 학과별 논문 수 (막대)
        6. 과정별 학생 수 (파이)
        7. 학과별 학생 수 (막대)
        8. 집행 항목별 비율 (파이)
        9. 지원 기관별 연구비 (막대)

        Args:
            year: 조회 연도
            college: 단과대학 (None이면 전체)

        Returns:
            Dict: {...}
        """
        # 1. 학과별 취업률
        dept_employment = self.dept_kpi_repo.get_by_department(year, college)

        # 2-3. 연도별 추이 (최근 3년)
        trend_data = self.dept_kpi_repo.get_trend_by_year(year - 2, year, college)

        # 4. SCIE/KCI 논문 분포
        paper_distribution = self.publication_repo.get_grade_distribution(year)

        # 5. 학과별 논문 수
        papers_by_dept = self.publication_repo.get_by_department(year)

        # 6. 과정별 학생 수
        students_by_program = self.student_repo.get_by_program('재학')

        # 7. 학과별 학생 수
        students_by_dept = self.student_repo.get_count_by_department('재학')

        # 8. 집행 항목별 비율
        budget_by_item = self.research_project_repo.get_by_item()

        # 9. 지원 기관별 연구비
        budget_by_agency = self.research_project_repo.get_by_agency()

        return {
            'department_employment_rate': self.chart_builder.build_department_employment_rate(dept_employment),
            'faculty_trend': self.chart_builder.build_faculty_trend(trend_data),
            'tech_transfer_trend': self.chart_builder.build_tech_transfer_trend(trend_data),
            'paper_distribution': self.chart_builder.build_paper_distribution(paper_distribution),
            'papers_by_department': self.chart_builder.build_papers_by_department(papers_by_dept),
            'students_by_program': self.chart_builder.build_students_by_program(students_by_program),
            'students_by_department': self.chart_builder.build_students_by_department(students_by_dept),
            'budget_by_item': self.chart_builder.build_budget_by_item(budget_by_item),
            'budget_by_funder': self.chart_builder.build_budget_by_funder(budget_by_agency)
        }

    def _safe_calculate_change_rate(self, current: Decimal, previous: Decimal) -> Decimal:
        """
        안전한 증감률 계산 (이전 값이 0일 경우 0 반환)

        Args:
            current: 현재 값
            previous: 이전 값

        Returns:
            Decimal: 증감률 (%)
        """
        if previous == Decimal('0') or previous == 0:
            return Decimal('0.0')

        try:
            return self.metric_calculator.calculate_change_rate(current, previous)
        except ValueError:
            return Decimal('0.0')
