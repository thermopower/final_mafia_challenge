# -*- coding: utf-8 -*-
"""
Performance Repository

실적 데이터 접근 계층
"""
from typing import List
from decimal import Decimal
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear

from apps.core.repositories.base_repository import BaseRepository
from apps.dashboard.persistence.models import Performance as PerformanceORM
from apps.dashboard.domain.models import Performance, PerformanceSummary


class PerformanceRepository(BaseRepository):
    """
    실적 Repository

    ORM 쿼리를 도메인 모델로 변환합니다.
    """
    model = PerformanceORM

    def get_summary_by_year(self, year: int, department: str = 'all') -> PerformanceSummary:
        """
        연도별 실적 요약 조회

        Args:
            year: 조회할 연도
            department: 부서명 (기본값: 'all')

        Returns:
            PerformanceSummary: 총액, 건수, 연도
        """
        queryset = self.model.objects.filter(is_deleted=False)

        # 연도 필터
        queryset = queryset.filter(date__year=year)

        # 부서 필터 (department 필드가 있다고 가정)
        # if department != 'all':
        #     queryset = queryset.filter(department=department)

        # 집계
        aggregation = queryset.aggregate(
            total_amount=Sum('amount'),
            count=Count('id')
        )

        return PerformanceSummary(
            total_amount=aggregation['total_amount'] or Decimal('0.0'),
            count=aggregation['count'] or 0,
            year=year
        )

    def get_monthly_trend(self, year: int, department: str = 'all') -> List[Performance]:
        """
        월별 실적 추세 조회

        Args:
            year: 조회할 연도
            department: 부서명 (기본값: 'all')

        Returns:
            List[Performance]: 월별 실적 리스트 (1월부터 12월 순서)
        """
        queryset = self.model.objects.filter(
            is_deleted=False,
            date__year=year
        )

        # if department != 'all':
        #     queryset = queryset.filter(department=department)

        performances = queryset.order_by('date')

        return [self._to_domain(perf) for perf in performances]

    def _to_domain(self, orm_obj: PerformanceORM) -> Performance:
        """ORM 모델 → 도메인 모델 변환"""
        return Performance(
            id=orm_obj.id,
            year=orm_obj.date.year,
            month=orm_obj.date.month,
            department='',  # 임시
            amount=orm_obj.amount,
            category=orm_obj.category
        )

    def bulk_create(self, performances: List[dict], user_id: str) -> int:
        """
        실적 데이터 배치 생성

        Args:
            performances: 실적 데이터 리스트 (파싱된 딕셔너리)
            user_id: 업로드한 사용자 ID

        Returns:
            int: 생성된 행 수
        """
        from apps.accounts.persistence.models import UserProfile

        user = UserProfile.objects.get(id=user_id)

        performance_objs = [
            PerformanceORM(
                date=perf['date'],
                title=perf.get('title', perf.get('항목', '')),
                amount=perf['amount'],
                category=perf['category'],
                description=perf.get('description', perf.get('비고', '')),
                uploaded_by=user
            )
            for perf in performances
        ]

        PerformanceORM.objects.bulk_create(performance_objs)
        return len(performance_objs)

    def check_duplicates(self, performances: List[dict]) -> List[dict]:
        """
        중복 데이터 확인

        Args:
            performances: 실적 데이터 리스트

        Returns:
            List[dict]: 중복된 데이터 리스트
        """
        duplicates = []

        for perf in performances:
            exists = PerformanceORM.objects.filter(
                date=perf['date'],
                title=perf.get('title', perf.get('항목', '')),
                is_deleted=False
            ).exists()

            if exists:
                duplicates.append(perf)

        return duplicates

    def _to_orm(self, domain_obj: Performance) -> PerformanceORM:
        """도메인 모델 → ORM 모델 변환"""
        # 이 메서드는 create/update 시 사용
        pass
