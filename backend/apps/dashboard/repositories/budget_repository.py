# -*- coding: utf-8 -*-
"""
Budget Repository

예산 데이터 접근 계층
"""
from typing import List
from decimal import Decimal
from django.db.models import Sum, Count

from apps.core.repositories.base_repository import BaseRepository
from apps.dashboard.persistence.models import Budget as BudgetORM
from apps.dashboard.domain.models import Budget, BudgetRatio


class BudgetRepository(BaseRepository):
    """
    예산 Repository

    ORM 쿼리를 도메인 모델로 변환합니다.
    """
    model = BudgetORM

    def get_total_by_year(self, year: int, department: str = 'all') -> Decimal:
        """
        연도별 예산 총액 조회

        Args:
            year: 조회할 연도 (회계연도)
            department: 부서명 (기본값: 'all')

        Returns:
            Decimal: 총 예산 금액
        """
        queryset = self.model.objects.filter(
            is_deleted=False,
            fiscal_year=year
        )

        # if department != 'all':
        #     queryset = queryset.filter(department=department)

        aggregation = queryset.aggregate(
            total_amount=Sum('amount')
        )

        return aggregation['total_amount'] or Decimal('0.0')

    def get_execution_rate(self, year: int, department: str = 'all') -> Decimal:
        """
        예산 집행률 조회

        현재는 단순히 총액을 반환합니다.
        실제로는 executed_amount / allocated_amount * 100을 계산해야 하지만,
        현재 모델에는 allocated_amount 필드가 없으므로 임시로 총액을 반환합니다.

        Args:
            year: 조회할 연도
            department: 부서명 (기본값: 'all')

        Returns:
            Decimal: 예산 집행률 (%)
        """
        total = self.get_total_by_year(year, department)

        # 임시로 총액을 반환 (추후 실제 집행률 로직으로 교체)
        return total

    def get_ratio_by_category(self, year: int, department: str = 'all') -> List[BudgetRatio]:
        """
        카테고리별 예산 비율 조회

        Args:
            year: 조회할 연도
            department: 부서명 (기본값: 'all')

        Returns:
            List[BudgetRatio]: 카테고리별 예산 비율 리스트
        """
        queryset = self.model.objects.filter(
            is_deleted=False,
            fiscal_year=year
        )

        # if department != 'all':
        #     queryset = queryset.filter(department=department)

        # 카테고리별 집계
        distribution = queryset.values('category').annotate(
            total_amount=Sum('amount')
        ).order_by('-total_amount')

        # 전체 총액 계산
        total_amount = self.get_total_by_year(year, department)

        result = []
        for item in distribution:
            amount = item['total_amount']
            percentage = (amount / total_amount * Decimal('100.0')) if total_amount > 0 else Decimal('0.0')

            result.append(
                BudgetRatio(
                    category=item['category'],
                    amount=amount,
                    percentage=round(percentage, 1)
                )
            )

        return result

    def get_all_by_year(self, year: int, department: str = 'all') -> List[Budget]:
        """
        연도별 예산 전체 조회

        Args:
            year: 조회할 연도
            department: 부서명 (기본값: 'all')

        Returns:
            List[Budget]: 예산 리스트
        """
        queryset = self.model.objects.filter(
            is_deleted=False,
            fiscal_year=year
        )

        # if department != 'all':
        #     queryset = queryset.filter(department=department)

        budgets = queryset.order_by('category')

        return [self._to_domain(budget) for budget in budgets]

    def _to_domain(self, orm_obj: BudgetORM) -> Budget:
        """ORM 모델 → 도메인 모델 변환"""
        return Budget(
            id=orm_obj.id,
            category=orm_obj.category,
            amount=orm_obj.amount
        )

    def bulk_create(self, budgets: List[dict], user_id: str) -> int:
        """
        예산 데이터 배치 생성

        Args:
            budgets: 예산 데이터 리스트 (파싱된 딕셔너리)
            user_id: 업로드한 사용자 ID

        Returns:
            int: 생성된 행 수
        """
        from apps.accounts.persistence.models import UserProfile

        user = UserProfile.objects.get(id=user_id)

        budget_objs = [
            BudgetORM(
                item=budget['item'],
                amount=budget['amount'],
                category=budget['category'],
                fiscal_year=budget['fiscal_year'],
                quarter=budget.get('quarter'),
                description=budget.get('description', budget.get('비고', '')),
                uploaded_by=user
            )
            for budget in budgets
        ]

        BudgetORM.objects.bulk_create(budget_objs)
        return len(budget_objs)

    def check_duplicates(self, budgets: List[dict]) -> List[dict]:
        """
        중복 데이터 확인

        Args:
            budgets: 예산 데이터 리스트

        Returns:
            List[dict]: 중복된 데이터 리스트
        """
        duplicates = []

        for budget in budgets:
            exists = BudgetORM.objects.filter(
                item=budget['item'],
                fiscal_year=budget['fiscal_year'],
                is_deleted=False
            ).exists()

            if exists:
                duplicates.append(budget)

        return duplicates

    def _to_orm(self, domain_obj: Budget) -> BudgetORM:
        """도메인 모델 → ORM 모델 변환"""
        # 이 메서드는 create/update 시 사용
        pass
