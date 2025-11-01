# -*- coding: utf-8 -*-
"""
Dashboard Service

대시보드 비즈니스 로직
"""
from typing import Dict, List
from decimal import Decimal

from apps.dashboard.domain.models import DashboardData, KPI
from apps.dashboard.repositories.performance_repository import PerformanceRepository
from apps.dashboard.repositories.paper_repository import PaperRepository
from apps.dashboard.repositories.student_repository import StudentRepository
from apps.dashboard.repositories.budget_repository import BudgetRepository
from apps.dashboard.services.metric_calculator import MetricCalculator
from apps.dashboard.services.chart_data_builder import ChartDataBuilder


class DashboardService:
    """
    대시보드 서비스

    여러 Repository를 조합하여 대시보드 데이터를 생성합니다.
    """

    def __init__(
        self,
        performance_repo: PerformanceRepository = None,
        paper_repo: PaperRepository = None,
        student_repo: StudentRepository = None,
        budget_repo: BudgetRepository = None,
        metric_calculator: MetricCalculator = None,
        chart_builder: ChartDataBuilder = None
    ):
        self.performance_repo = performance_repo or PerformanceRepository()
        self.paper_repo = paper_repo or PaperRepository()
        self.student_repo = student_repo or StudentRepository()
        self.budget_repo = budget_repo or BudgetRepository()
        self.metric_calculator = metric_calculator or MetricCalculator()
        self.chart_builder = chart_builder or ChartDataBuilder()

    def get_dashboard_data(self, year: int, department: str) -> DashboardData:
        """
        대시보드 전체 데이터 조회 및 생성

        Args:
            year: 조회할 연도
            department: 부서명

        Returns:
            DashboardData: KPI, 차트, 필터 정보를 포함한 대시보드 데이터
        """
        kpis = self._build_kpis(year, department)
        charts = self._build_charts(year, department)
        filters = {'year': year, 'department': department}

        return DashboardData(kpis=kpis, charts=charts, filters=filters)

    def _build_kpis(self, year: int, department: str) -> Dict[str, KPI]:
        """
        KPI 데이터 생성 (병렬 조회 및 증감률 계산)

        Args:
            year: 조회할 연도
            department: 부서명

        Returns:
            Dict[str, KPI]: KPI 딕셔너리
        """
        # 현재 연도 데이터 조회
        current_perf = self.performance_repo.get_summary_by_year(year, department)
        current_paper_count = self.paper_repo.get_count_by_year(year, department)
        current_student_count = self.student_repo.get_count_by_year(year, department)
        current_budget_rate = self.budget_repo.get_execution_rate(year, department)

        # 이전 연도 데이터 조회
        previous_year = year - 1
        previous_perf = self.performance_repo.get_summary_by_year(previous_year, department)
        previous_paper_count = self.paper_repo.get_count_by_year(previous_year, department)
        previous_student_count = self.student_repo.get_count_by_year(previous_year, department)
        previous_budget_rate = self.budget_repo.get_execution_rate(previous_year, department)

        # 증감률 계산
        perf_change = self.metric_calculator.calculate_change_rate(
            current_perf.total_amount, previous_perf.total_amount
        ) if previous_perf.total_amount > 0 else Decimal('0.0')

        paper_change = self.metric_calculator.calculate_change_rate(
            Decimal(str(current_paper_count)), Decimal(str(previous_paper_count))
        ) if previous_paper_count > 0 else Decimal('0.0')

        student_change = self.metric_calculator.calculate_change_rate(
            Decimal(str(current_student_count)), Decimal(str(previous_student_count))
        ) if previous_student_count > 0 else Decimal('0.0')

        budget_change = self.metric_calculator.calculate_change_rate(
            current_budget_rate, previous_budget_rate
        ) if previous_budget_rate > 0 else Decimal('0.0')

        return {
            'performance': KPI(
                value=current_perf.total_amount,
                unit='억원',
                change_rate=perf_change,
                trend=self.metric_calculator.determine_trend(perf_change)
            ),
            'papers': KPI(
                value=Decimal(str(current_paper_count)),
                unit='편',
                change_rate=paper_change,
                trend=self.metric_calculator.determine_trend(paper_change)
            ),
            'students': KPI(
                value=Decimal(str(current_student_count)),
                unit='명',
                change_rate=student_change,
                trend=self.metric_calculator.determine_trend(student_change)
            ),
            'budget': KPI(
                value=current_budget_rate,
                unit='%',
                change_rate=budget_change,
                trend=self.metric_calculator.determine_trend(budget_change)
            )
        }

    def _build_charts(self, year: int, department: str) -> Dict[str, List[Dict]]:
        """
        차트 데이터 생성

        Args:
            year: 조회할 연도
            department: 부서명

        Returns:
            Dict[str, List[Dict]]: 차트 데이터 딕셔너리
        """
        performances = self.performance_repo.get_monthly_trend(year, department)
        paper_distribution = self.paper_repo.get_distribution_by_category(year, department)
        budget_ratios = self.budget_repo.get_ratio_by_category(year, department)
        student_counts = self.student_repo.get_count_by_department(year)

        return {
            'performance_trend': self.chart_builder.build_performance_trend(performances),
            'paper_distribution': self.chart_builder.build_paper_distribution(paper_distribution),
            'budget_ratio': self.chart_builder.build_budget_ratio(budget_ratios),
            'student_count': self.chart_builder.build_student_count(student_counts)
        }
