# -*- coding: utf-8 -*-
"""
Dashboard Service 계층 단위 테스트

TDD Red-Green-Refactor 사이클을 따릅니다.
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock

from apps.dashboard.domain.models import (
    PerformanceSummary,
    PaperCount,
    StudentCount,
    BudgetRatio,
    Performance,
    Paper,
    Student,
    Budget
)


class TestMetricCalculator:
    """MetricCalculator 테스트"""

    def test_calculate_change_rate_with_positive_change(self):
        """양수 증감률 계산 테스트"""
        # Arrange
        from apps.dashboard.services.metric_calculator import MetricCalculator
        current_value = Decimal('112.3')
        previous_value = Decimal('100.0')

        # Act
        change_rate = MetricCalculator.calculate_change_rate(current_value, previous_value)

        # Assert
        assert change_rate == Decimal('12.3')

    def test_calculate_change_rate_with_negative_change(self):
        """음수 증감률 계산 테스트"""
        # Arrange
        from apps.dashboard.services.metric_calculator import MetricCalculator
        current_value = Decimal('90.0')
        previous_value = Decimal('100.0')

        # Act
        change_rate = MetricCalculator.calculate_change_rate(current_value, previous_value)

        # Assert
        assert change_rate == Decimal('-10.0')

    def test_calculate_change_rate_with_zero_previous_value_raises_error(self):
        """이전 값이 0일 때 예외 발생 테스트"""
        # Arrange
        from apps.dashboard.services.metric_calculator import MetricCalculator
        current_value = Decimal('100.0')
        previous_value = Decimal('0.0')

        # Act & Assert
        with pytest.raises(ValueError, match='이전 값은 0이 될 수 없습니다'):
            MetricCalculator.calculate_change_rate(current_value, previous_value)

    def test_determine_trend_returns_up_for_positive_rate(self):
        """양수 증감률 → 'up' 반환 테스트"""
        # Arrange
        from apps.dashboard.services.metric_calculator import MetricCalculator
        change_rate = Decimal('12.3')

        # Act
        trend = MetricCalculator.determine_trend(change_rate)

        # Assert
        assert trend == 'up'

    def test_determine_trend_returns_down_for_negative_rate(self):
        """음수 증감률 → 'down' 반환 테스트"""
        # Arrange
        from apps.dashboard.services.metric_calculator import MetricCalculator
        change_rate = Decimal('-5.2')

        # Act
        trend = MetricCalculator.determine_trend(change_rate)

        # Assert
        assert trend == 'down'

    def test_determine_trend_returns_neutral_for_zero_rate(self):
        """0 증감률 → 'neutral' 반환 테스트"""
        # Arrange
        from apps.dashboard.services.metric_calculator import MetricCalculator
        change_rate = Decimal('0.0')

        # Act
        trend = MetricCalculator.determine_trend(change_rate)

        # Assert
        assert trend == 'neutral'


class TestChartDataBuilder:
    """ChartDataBuilder 테스트"""

    def test_build_performance_trend_transforms_correctly(self):
        """실적 추세 차트 데이터 변환 테스트"""
        # Arrange
        from apps.dashboard.services.chart_data_builder import ChartDataBuilder
        performances = [
            Performance(id=1, year=2024, month=1, department='CS', amount=Decimal('10.5'), category='연구비'),
            Performance(id=2, year=2024, month=2, department='CS', amount=Decimal('12.3'), category='연구비'),
        ]
        builder = ChartDataBuilder()

        # Act
        chart_data = builder.build_performance_trend(performances)

        # Assert
        assert len(chart_data) == 2
        assert chart_data[0]['month'] == '1월'
        assert chart_data[0]['value'] == Decimal('10.5')
        assert chart_data[1]['month'] == '2월'
        assert chart_data[1]['value'] == Decimal('12.3')

    def test_build_paper_distribution_groups_by_category(self):
        """논문 분포 차트 데이터 생성 테스트"""
        # Arrange
        from apps.dashboard.services.chart_data_builder import ChartDataBuilder
        paper_counts = [
            PaperCount(category='SCI', count=20),
            PaperCount(category='KCI', count=15),
            PaperCount(category='기타', count=5),
        ]
        builder = ChartDataBuilder()

        # Act
        chart_data = builder.build_paper_distribution(paper_counts)

        # Assert
        assert len(chart_data) == 3
        assert chart_data[0]['category'] == 'SCI'
        assert chart_data[0]['count'] == 20

    def test_build_budget_ratio_includes_percentage(self):
        """예산 비율 차트 데이터 생성 테스트"""
        # Arrange
        from apps.dashboard.services.chart_data_builder import ChartDataBuilder
        budget_ratios = [
            BudgetRatio(category='인건비', amount=Decimal('50.0'), percentage=Decimal('50.0')),
            BudgetRatio(category='연구비', amount=Decimal('30.0'), percentage=Decimal('30.0')),
            BudgetRatio(category='운영비', amount=Decimal('20.0'), percentage=Decimal('20.0')),
        ]
        builder = ChartDataBuilder()

        # Act
        chart_data = builder.build_budget_ratio(budget_ratios)

        # Assert
        assert len(chart_data) == 3
        assert chart_data[0]['category'] == '인건비'
        assert chart_data[0]['value'] == Decimal('50.0')
        assert chart_data[0]['percentage'] == Decimal('50.0')

    def test_build_student_count_transforms_correctly(self):
        """학생 수 차트 데이터 변환 테스트"""
        # Arrange
        from apps.dashboard.services.chart_data_builder import ChartDataBuilder
        student_counts = [
            StudentCount(department='컴퓨터공학과', count=450),
            StudentCount(department='전자공학과', count=380),
        ]
        builder = ChartDataBuilder()

        # Act
        chart_data = builder.build_student_count(student_counts)

        # Assert
        assert len(chart_data) == 2
        assert chart_data[0]['department'] == '컴퓨터공학과'
        assert chart_data[0]['count'] == 450


class TestDashboardService:
    """DashboardService 테스트 (Mock 사용)"""

    def test_build_kpis_calculates_change_rate_correctly(self):
        """KPI 생성 및 증감률 계산 테스트"""
        # Arrange
        from apps.dashboard.services.dashboard_service import DashboardService

        # Mock Repositories
        mock_perf_repo = Mock()
        mock_perf_repo.get_summary_by_year.side_effect = [
            PerformanceSummary(total_amount=Decimal('150.5'), count=10, year=2024),
            PerformanceSummary(total_amount=Decimal('100.0'), count=8, year=2023)
        ]

        mock_paper_repo = Mock()
        mock_paper_repo.get_count_by_year.side_effect = [245, 258]  # 2024, 2023

        mock_student_repo = Mock()
        mock_student_repo.get_count_by_year.side_effect = [1850, 1795]

        mock_budget_repo = Mock()
        mock_budget_repo.get_execution_rate.side_effect = [Decimal('87.5'), Decimal('87.5')]

        service = DashboardService(
            performance_repo=mock_perf_repo,
            paper_repo=mock_paper_repo,
            student_repo=mock_student_repo,
            budget_repo=mock_budget_repo
        )

        # Act
        kpis = service._build_kpis(year=2024, department='all')

        # Assert
        assert 'performance' in kpis
        assert kpis['performance'].value == Decimal('150.5')
        assert kpis['performance'].change_rate == Decimal('50.5')
        assert kpis['performance'].trend == 'up'

        assert 'papers' in kpis
        assert kpis['papers'].value == Decimal('245')
        # 245 vs 258 → -5.0% 변화
        assert kpis['papers'].trend == 'down'

    def test_get_dashboard_data_returns_complete_structure(self):
        """대시보드 데이터 전체 구조 반환 테스트"""
        # Arrange
        from apps.dashboard.services.dashboard_service import DashboardService

        # Mock Repositories
        mock_perf_repo = Mock()
        mock_perf_repo.get_summary_by_year.side_effect = [
            PerformanceSummary(total_amount=Decimal('150.5'), count=10, year=2024),
            PerformanceSummary(total_amount=Decimal('100.0'), count=8, year=2023)
        ]
        mock_perf_repo.get_monthly_trend.return_value = [
            Performance(id=1, year=2024, month=1, department='CS', amount=Decimal('10.0'), category='연구비')
        ]
        mock_perf_repo.get_all_by_year.return_value = []

        mock_paper_repo = Mock()
        mock_paper_repo.get_count_by_year.side_effect = [245, 258]
        mock_paper_repo.get_distribution_by_category.return_value = [
            PaperCount(category='SCI', count=120)
        ]
        mock_paper_repo.get_all_by_year.return_value = []

        mock_student_repo = Mock()
        mock_student_repo.get_count_by_year.side_effect = [1850, 1795]
        mock_student_repo.get_count_by_department.return_value = [
            StudentCount(department='컴퓨터공학과', count=450)
        ]
        mock_student_repo.get_all_by_year.return_value = []

        mock_budget_repo = Mock()
        mock_budget_repo.get_execution_rate.side_effect = [Decimal('87.5'), Decimal('87.5')]
        mock_budget_repo.get_ratio_by_category.return_value = [
            BudgetRatio(category='인건비', amount=Decimal('50.0'), percentage=Decimal('50.0'))
        ]
        mock_budget_repo.get_all_by_year.return_value = []

        service = DashboardService(
            performance_repo=mock_perf_repo,
            paper_repo=mock_paper_repo,
            student_repo=mock_student_repo,
            budget_repo=mock_budget_repo
        )

        # Act
        dashboard_data = service.get_dashboard_data(year=2024, department='all')

        # Assert
        assert 'performance' in dashboard_data.kpis
        assert 'papers' in dashboard_data.kpis
        assert 'students' in dashboard_data.kpis
        assert 'budget' in dashboard_data.kpis
        assert 'performance_trend' in dashboard_data.charts
        assert 'paper_distribution' in dashboard_data.charts
        assert 'budget_ratio' in dashboard_data.charts
        assert 'student_count' in dashboard_data.charts
        assert dashboard_data.filters['year'] == 2024
        assert dashboard_data.filters['department'] == 'all'
