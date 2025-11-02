# -*- coding: utf-8 -*-
"""
DepartmentKPI Repository

학과 KPI 데이터 접근 계층
"""
from typing import List, Dict, Optional
from decimal import Decimal
from django.db.models import Avg, Sum
from django.db import transaction

from apps.dashboard.persistence.models import DepartmentKPI


class DepartmentKPIRepository:
    """
    학과 KPI 데이터 Repository

    데이터베이스 CRUD 작업 및 통계 조회를 제공합니다.
    """

    @staticmethod
    def bulk_create(data_list: List[Dict]) -> int:
        """
        대량 데이터 삽입

        Args:
            data_list: 삽입할 데이터 리스트
                [
                    {
                        'evaluation_year': 2024,
                        'college': '공과대학',
                        'department': '컴퓨터공학과',
                        'employment_rate': Decimal('87.5'),
                        'full_time_faculty': 35,
                        'visiting_faculty': 12,
                        'tech_transfer_income': Decimal('2.5'),
                        'intl_conferences': 3
                    },
                    ...
                ]

        Returns:
            int: 삽입된 행 수
        """
        if not data_list:
            return 0

        with transaction.atomic():
            objects = [DepartmentKPI(**data) for data in data_list]
            created = DepartmentKPI.objects.bulk_create(
                objects,
                ignore_conflicts=False  # 중복 시 에러 발생
            )
            return len(created)

    @staticmethod
    def get_summary(year: Optional[int] = None, college: Optional[str] = None) -> Dict:
        """
        KPI 요약 통계 조회

        Args:
            year: 평가년도 (None이면 전체)
            college: 단과대학 (None이면 전체)

        Returns:
            Dict: 요약 통계
                {
                    'avg_employment_rate': Decimal,
                    'total_full_time_faculty': int,
                    'total_visiting_faculty': int,
                    'total_tech_transfer_income': Decimal,
                    'total_intl_conferences': int
                }
        """
        queryset = DepartmentKPI.objects.all()

        if year:
            queryset = queryset.filter(evaluation_year=year)

        if college:
            queryset = queryset.filter(college=college)

        stats = queryset.aggregate(
            avg_employment_rate=Avg('employment_rate'),
            total_full_time_faculty=Sum('full_time_faculty'),
            total_visiting_faculty=Sum('visiting_faculty'),
            total_tech_transfer_income=Sum('tech_transfer_income'),
            total_intl_conferences=Sum('intl_conferences')
        )

        # None 값을 0 또는 Decimal('0')으로 변환
        return {
            'avg_employment_rate': stats['avg_employment_rate'] or Decimal('0'),
            'total_full_time_faculty': stats['total_full_time_faculty'] or 0,
            'total_visiting_faculty': stats['total_visiting_faculty'] or 0,
            'total_tech_transfer_income': stats['total_tech_transfer_income'] or Decimal('0'),
            'total_intl_conferences': stats['total_intl_conferences'] or 0
        }

    @staticmethod
    def get_by_college(year: int) -> List[Dict]:
        """
        단과대학별 KPI 조회

        Args:
            year: 평가년도

        Returns:
            List[Dict]: 단과대학별 데이터
                [
                    {
                        'college': '공과대학',
                        'avg_employment_rate': Decimal,
                        'total_faculty': int
                    },
                    ...
                ]
        """
        from django.db.models import F, Value
        from django.db.models.functions import Coalesce

        queryset = DepartmentKPI.objects.filter(
            evaluation_year=year
        ).values(
            'college'
        ).annotate(
            avg_employment_rate=Coalesce(Avg('employment_rate'), Value(Decimal('0'))),
            total_faculty=Coalesce(Sum('full_time_faculty'), Value(0))
        ).order_by('college')

        return list(queryset)

    @staticmethod
    def get_by_department(year: int, college: Optional[str] = None) -> List[Dict]:
        """
        학과별 KPI 조회 (차트용)

        Args:
            year: 평가년도
            college: 단과대학 (None이면 전체)

        Returns:
            List[Dict]: 학과별 데이터
                [
                    {
                        'department': '컴퓨터공학과',
                        'employment_rate': Decimal('87.5')
                    },
                    ...
                ]
        """
        queryset = DepartmentKPI.objects.filter(evaluation_year=year)

        if college and college != 'all':
            queryset = queryset.filter(college=college)

        result = queryset.values('department', 'employment_rate').order_by('department')

        return list(result)

    @staticmethod
    def get_trend_by_year(start_year: int, end_year: int, college: Optional[str] = None) -> List[Dict]:
        """
        연도별 추이 데이터 조회

        Args:
            start_year: 시작 연도
            end_year: 종료 연도
            college: 단과대학 (None이면 전체)

        Returns:
            List[Dict]: 연도별 집계 데이터
                [
                    {
                        'evaluation_year': 2024,
                        'total_full_time_faculty': 150,
                        'total_visiting_faculty': 30,
                        'total_tech_transfer_income': Decimal('120.0')
                    },
                    ...
                ]
        """
        queryset = DepartmentKPI.objects.filter(
            evaluation_year__gte=start_year,
            evaluation_year__lte=end_year
        )

        if college and college != 'all':
            queryset = queryset.filter(college=college)

        result = queryset.values('evaluation_year').annotate(
            total_full_time_faculty=Sum('full_time_faculty'),
            total_visiting_faculty=Sum('visiting_faculty'),
            total_tech_transfer_income=Sum('tech_transfer_income')
        ).order_by('evaluation_year')

        return list(result)

    @staticmethod
    def delete_by_year(year: int) -> int:
        """
        특정 연도의 데이터 삭제

        Args:
            year: 평가년도

        Returns:
            int: 삭제된 행 수
        """
        deleted_count, _ = DepartmentKPI.objects.filter(
            evaluation_year=year
        ).delete()

        return deleted_count
