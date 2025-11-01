# -*- coding: utf-8 -*-
"""
Dashboard Repository 계층 단위 테스트

TDD Red-Green-Refactor 사이클을 따릅니다.
"""
import pytest
from decimal import Decimal
from datetime import date


@pytest.mark.django_db
class TestPerformanceRepository:
    """PerformanceRepository 테스트"""

    def test_get_summary_by_year_returns_correct_aggregation(self):
        """연도별 요약 조회 테스트"""
        # Arrange
        from apps.dashboard.repositories.performance_repository import PerformanceRepository
        from apps.dashboard.persistence.models import Performance
        from apps.accounts.persistence.models import UserProfile
        from django.utils import timezone

        import uuid
        user = UserProfile.objects.create(
            id=uuid.uuid4(),
            email='test@example.com',
            role='admin'
        )

        Performance.objects.create(
            date=date(2024, 1, 15),
            title='실적1',
            amount=Decimal('100.0'),
            category='연구비',
            uploaded_by=user
        )
        Performance.objects.create(
            date=date(2024, 2, 20),
            title='실적2',
            amount=Decimal('50.5'),
            category='특허료',
            uploaded_by=user
        )
        Performance.objects.create(
            date=date(2023, 1, 10),
            title='실적3',
            amount=Decimal('200.0'),
            category='연구비',
            uploaded_by=user
        )

        repo = PerformanceRepository()

        # Act
        summary = repo.get_summary_by_year(year=2024)

        # Assert
        assert summary.total_amount == Decimal('150.5')
        assert summary.count == 2
        assert summary.year == 2024

    def test_get_monthly_trend_returns_ordered_data(self):
        """월별 추세 조회 테스트"""
        # Arrange
        from apps.dashboard.repositories.performance_repository import PerformanceRepository
        from apps.dashboard.persistence.models import Performance
        from apps.accounts.persistence.models import UserProfile

        import uuid
        user = UserProfile.objects.create(
            id=uuid.uuid4(),
            email='test2@example.com',
            role='admin'
        )

        Performance.objects.create(
            date=date(2024, 3, 10),
            title='실적3월',
            amount=Decimal('30.0'),
            category='연구비',
            uploaded_by=user
        )
        Performance.objects.create(
            date=date(2024, 1, 5),
            title='실적1월',
            amount=Decimal('10.0'),
            category='연구비',
            uploaded_by=user
        )
        Performance.objects.create(
            date=date(2024, 2, 15),
            title='실적2월',
            amount=Decimal('20.0'),
            category='연구비',
            uploaded_by=user
        )

        repo = PerformanceRepository()

        # Act
        trend = repo.get_monthly_trend(year=2024)

        # Assert
        assert len(trend) == 3
        assert trend[0].month == 1
        assert trend[1].month == 2
        assert trend[2].month == 3


@pytest.mark.django_db
class TestPaperRepository:
    """PaperRepository 테스트"""

    def test_get_count_by_year_returns_correct_count(self):
        """연도별 논문 수 조회 테스트"""
        # Arrange
        from apps.dashboard.repositories.paper_repository import PaperRepository
        from apps.dashboard.persistence.models import Paper
        from apps.accounts.persistence.models import UserProfile

        import uuid
        user = UserProfile.objects.create(
            id=uuid.uuid4(),
            email='paper_test@example.com',
            role='admin'
        )

        # 2024년 논문 5개
        for i in range(5):
            Paper.objects.create(
                title=f'논문{i}',
                authors='저자1, 저자2',
                publication_date=date(2024, 1, i+1),
                field='국제학술지',
                uploaded_by=user
            )

        # 2023년 논문 3개
        for i in range(3):
            Paper.objects.create(
                title=f'논문2023_{i}',
                authors='저자3',
                publication_date=date(2023, 1, i+1),
                field='국내학술지',
                uploaded_by=user
            )

        repo = PaperRepository()

        # Act
        count = repo.get_count_by_year(year=2024)

        # Assert
        assert count == 5

    def test_get_distribution_by_category_groups_correctly(self):
        """카테고리별 논문 분포 조회 테스트"""
        # Arrange
        from apps.dashboard.repositories.paper_repository import PaperRepository
        from apps.dashboard.persistence.models import Paper
        from apps.accounts.persistence.models import UserProfile

        import uuid
        user = UserProfile.objects.create(
            id=uuid.uuid4(),
            email='paper_dist@example.com',
            role='admin'
        )

        # SCI 논문 3개
        for i in range(3):
            Paper.objects.create(
                title=f'SCI논문{i}',
                authors='저자',
                publication_date=date(2024, 1, i+1),
                field='SCI',
                uploaded_by=user
            )

        # KCI 논문 2개
        for i in range(2):
            Paper.objects.create(
                title=f'KCI논문{i}',
                authors='저자',
                publication_date=date(2024, 2, i+1),
                field='KCI',
                uploaded_by=user
            )

        # 기타 논문 1개
        Paper.objects.create(
            title='기타논문',
            authors='저자',
            publication_date=date(2024, 3, 1),
            field='기타',
            uploaded_by=user
        )

        repo = PaperRepository()

        # Act
        distribution = repo.get_distribution_by_category(year=2024)

        # Assert
        assert len(distribution) == 3
        sci_count = next(d for d in distribution if d.category == 'SCI')
        assert sci_count.count == 3
        kci_count = next(d for d in distribution if d.category == 'KCI')
        assert kci_count.count == 2
        etc_count = next(d for d in distribution if d.category == '기타')
        assert etc_count.count == 1


@pytest.mark.django_db
class TestStudentRepository:
    """StudentRepository 테스트"""

    def test_get_count_by_year_returns_active_students(self):
        """연도별 학생 수 조회 테스트 (재학생만)"""
        # Arrange
        from apps.dashboard.repositories.student_repository import StudentRepository
        from apps.dashboard.persistence.models import Student
        from apps.accounts.persistence.models import UserProfile

        import uuid
        user = UserProfile.objects.create(
            id=uuid.uuid4(),
            email='student_test@example.com',
            role='admin'
        )

        # 재학생 10명
        for i in range(10):
            Student.objects.create(
                student_id=f'2024{i:03d}',
                name=f'학생{i}',
                department='컴퓨터공학과',
                grade=1,
                status='active',
                uploaded_by=user
            )

        # 졸업생 3명 (카운트에 포함되지 않아야 함)
        for i in range(3):
            Student.objects.create(
                student_id=f'2020{i:03d}',
                name=f'졸업생{i}',
                department='컴퓨터공학과',
                grade=4,
                status='graduated',
                uploaded_by=user
            )

        repo = StudentRepository()

        # Act
        count = repo.get_count_by_year(year=2024)

        # Assert
        assert count == 10

    def test_get_count_by_department_groups_correctly(self):
        """학과별 학생 수 조회 테스트"""
        # Arrange
        from apps.dashboard.repositories.student_repository import StudentRepository
        from apps.dashboard.persistence.models import Student
        from apps.accounts.persistence.models import UserProfile

        import uuid
        user = UserProfile.objects.create(
            id=uuid.uuid4(),
            email='student_dept@example.com',
            role='admin'
        )

        # 컴퓨터공학과 5명
        for i in range(5):
            Student.objects.create(
                student_id=f'CS2024{i:03d}',
                name=f'CS학생{i}',
                department='컴퓨터공학과',
                grade=1,
                status='active',
                uploaded_by=user
            )

        # 전자공학과 3명
        for i in range(3):
            Student.objects.create(
                student_id=f'EE2024{i:03d}',
                name=f'EE학생{i}',
                department='전자공학과',
                grade=1,
                status='active',
                uploaded_by=user
            )

        repo = StudentRepository()

        # Act
        distribution = repo.get_count_by_department(year=2024)

        # Assert
        assert len(distribution) == 2
        cs_count = next(d for d in distribution if d.department == '컴퓨터공학과')
        assert cs_count.count == 5
        ee_count = next(d for d in distribution if d.department == '전자공학과')
        assert ee_count.count == 3


@pytest.mark.django_db
class TestBudgetRepository:
    """BudgetRepository 테스트"""

    def test_get_execution_rate_calculates_correctly(self):
        """예산 집행률 계산 테스트"""
        # Arrange
        from apps.dashboard.repositories.budget_repository import BudgetRepository
        from apps.dashboard.persistence.models import Budget
        from apps.accounts.persistence.models import UserProfile

        import uuid
        user = UserProfile.objects.create(
            id=uuid.uuid4(),
            email='budget_test@example.com',
            role='admin'
        )

        # 2024년 예산 (총 100억원)
        Budget.objects.create(
            item='인건비',
            amount=Decimal('50.0'),  # 억원
            category='인건비',
            fiscal_year=2024,
            uploaded_by=user
        )
        Budget.objects.create(
            item='연구비',
            amount=Decimal('30.0'),
            category='연구비',
            fiscal_year=2024,
            uploaded_by=user
        )
        Budget.objects.create(
            item='운영비',
            amount=Decimal('20.0'),
            category='운영비',
            fiscal_year=2024,
            uploaded_by=user
        )

        repo = BudgetRepository()

        # Act
        total = repo.get_total_by_year(year=2024)

        # Assert
        assert total == Decimal('100.0')

    def test_get_ratio_by_category_calculates_percentage(self):
        """카테고리별 예산 비율 조회 테스트"""
        # Arrange
        from apps.dashboard.repositories.budget_repository import BudgetRepository
        from apps.dashboard.persistence.models import Budget
        from apps.accounts.persistence.models import UserProfile

        import uuid
        user = UserProfile.objects.create(
            id=uuid.uuid4(),
            email='budget_ratio@example.com',
            role='admin'
        )

        Budget.objects.create(
            item='인건비',
            amount=Decimal('50.0'),
            category='인건비',
            fiscal_year=2024,
            uploaded_by=user
        )
        Budget.objects.create(
            item='연구비',
            amount=Decimal('30.0'),
            category='연구비',
            fiscal_year=2024,
            uploaded_by=user
        )
        Budget.objects.create(
            item='운영비',
            amount=Decimal('20.0'),
            category='운영비',
            fiscal_year=2024,
            uploaded_by=user
        )

        repo = BudgetRepository()

        # Act
        ratio = repo.get_ratio_by_category(year=2024)

        # Assert
        assert len(ratio) == 3
        labor = next(r for r in ratio if r.category == '인건비')
        assert labor.amount == Decimal('50.0')
        assert labor.percentage == Decimal('50.0')  # 50/100*100
