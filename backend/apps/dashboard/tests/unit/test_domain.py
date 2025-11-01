# -*- coding: utf-8 -*-
"""
Dashboard Domain 모델 단위 테스트

TDD Red-Green-Refactor 사이클을 따릅니다.
"""
import pytest
from decimal import Decimal


class TestKPIDomain:
    """KPI 도메인 모델 테스트"""

    def test_kpi_creation_with_valid_data(self):
        """유효한 데이터로 KPI 생성 테스트"""
        # Arrange & Act
        from apps.dashboard.domain.models import KPI

        kpi = KPI(
            value=Decimal('150.5'),
            unit='억원',
            change_rate=Decimal('12.3'),
            trend='up'
        )

        # Assert
        assert kpi.value == Decimal('150.5')
        assert kpi.unit == '억원'
        assert kpi.change_rate == Decimal('12.3')
        assert kpi.trend == 'up'

    def test_kpi_creation_with_down_trend(self):
        """감소 추세 KPI 생성 테스트"""
        # Arrange & Act
        from apps.dashboard.domain.models import KPI

        kpi = KPI(
            value=Decimal('245'),
            unit='편',
            change_rate=Decimal('-5.2'),
            trend='down'
        )

        # Assert
        assert kpi.value == Decimal('245')
        assert kpi.unit == '편'
        assert kpi.change_rate == Decimal('-5.2')
        assert kpi.trend == 'down'

    def test_kpi_creation_with_neutral_trend(self):
        """동일 추세 KPI 생성 테스트"""
        # Arrange & Act
        from apps.dashboard.domain.models import KPI

        kpi = KPI(
            value=Decimal('87.5'),
            unit='%',
            change_rate=Decimal('0.0'),
            trend='neutral'
        )

        # Assert
        assert kpi.value == Decimal('87.5')
        assert kpi.unit == '%'
        assert kpi.change_rate == Decimal('0.0')
        assert kpi.trend == 'neutral'


class TestDashboardDataDomain:
    """DashboardData 도메인 모델 테스트"""

    def test_dashboard_data_creation_with_all_fields(self):
        """모든 필드를 포함한 DashboardData 생성 테스트"""
        # Arrange
        from apps.dashboard.domain.models import DashboardData, KPI

        kpis = {
            'performance': KPI(Decimal('150.5'), '억원', Decimal('12.3'), 'up'),
            'papers': KPI(Decimal('245'), '편', Decimal('-5.2'), 'down'),
            'students': KPI(Decimal('1850'), '명', Decimal('3.1'), 'up'),
            'budget': KPI(Decimal('87.5'), '%', Decimal('0.0'), 'neutral')
        }
        charts = {
            'performance_trend': [{'month': '1월', 'value': 12.5}],
            'paper_distribution': [{'category': 'SCI', 'count': 120}],
            'budget_ratio': [{'category': '인건비', 'value': 45.2, 'percentage': 51.7}],
            'student_count': [{'department': '컴퓨터공학과', 'count': 450}]
        }
        filters = {'year': 2024, 'department': 'all'}

        # Act
        dashboard_data = DashboardData(kpis=kpis, charts=charts, filters=filters)

        # Assert
        assert dashboard_data.kpis['performance'].value == Decimal('150.5')
        assert len(dashboard_data.charts['performance_trend']) == 1
        assert dashboard_data.charts['performance_trend'][0]['month'] == '1월'
        assert dashboard_data.filters['year'] == 2024
        assert dashboard_data.filters['department'] == 'all'


class TestPerformanceSummaryDomain:
    """PerformanceSummary 도메인 모델 테스트"""

    def test_performance_summary_creation(self):
        """PerformanceSummary 생성 테스트"""
        # Arrange & Act
        from apps.dashboard.domain.models import PerformanceSummary

        summary = PerformanceSummary(
            total_amount=Decimal('150.5'),
            count=10,
            year=2024
        )

        # Assert
        assert summary.total_amount == Decimal('150.5')
        assert summary.count == 10
        assert summary.year == 2024


class TestPaperCountDomain:
    """PaperCount 도메인 모델 테스트"""

    def test_paper_count_creation(self):
        """PaperCount 생성 테스트"""
        # Arrange & Act
        from apps.dashboard.domain.models import PaperCount

        paper_count = PaperCount(
            category='SCI',
            count=120
        )

        # Assert
        assert paper_count.category == 'SCI'
        assert paper_count.count == 120


class TestStudentCountDomain:
    """StudentCount 도메인 모델 테스트"""

    def test_student_count_creation(self):
        """StudentCount 생성 테스트"""
        # Arrange & Act
        from apps.dashboard.domain.models import StudentCount

        student_count = StudentCount(
            department='컴퓨터공학과',
            count=450
        )

        # Assert
        assert student_count.department == '컴퓨터공학과'
        assert student_count.count == 450


class TestBudgetRatioDomain:
    """BudgetRatio 도메인 모델 테스트"""

    def test_budget_ratio_creation(self):
        """BudgetRatio 생성 테스트"""
        # Arrange & Act
        from apps.dashboard.domain.models import BudgetRatio

        budget_ratio = BudgetRatio(
            category='인건비',
            amount=Decimal('45.2'),
            percentage=Decimal('51.7')
        )

        # Assert
        assert budget_ratio.category == '인건비'
        assert budget_ratio.amount == Decimal('45.2')
        assert budget_ratio.percentage == Decimal('51.7')
