# -*- coding: utf-8 -*-
"""
ResearchProject Repository

연구 과제 데이터 접근 계층
"""
from typing import List, Dict, Optional
from django.db.models import Sum, Count, Q, Value, F
from django.db.models.functions import Coalesce
from django.db import transaction

from apps.dashboard.persistence.models import ResearchProject


class ResearchProjectRepository:
    """
    연구 과제 데이터 Repository

    데이터베이스 CRUD 작업 및 예산 통계를 제공합니다.
    """

    @staticmethod
    def bulk_create(data_list: List[Dict]) -> int:
        """
        대량 데이터 삽입

        Args:
            data_list: 삽입할 데이터 리스트
                [
                    {
                        'execution_id': 'T2301001',
                        'project_number': 'NRF-2023-015',
                        'project_name': '차세대 AI 반도체 설계',
                        'principal_investigator': '김민준',
                        'department': '컴퓨터공학과',
                        'funding_agency': '한국연구재단',
                        'total_budget': 500000000,
                        'execution_date': date(2024, 3, 15),
                        'execution_item': '연구장비 도입',
                        'execution_amount': 150000000,
                        'status': '집행완료',
                        'remarks': '특수장비 구입'
                    },
                    ...
                ]

        Returns:
            int: 삽입된 행 수
        """
        if not data_list:
            return 0

        with transaction.atomic():
            objects = [ResearchProject(**data) for data in data_list]
            created = ResearchProject.objects.bulk_create(
                objects,
                ignore_conflicts=False  # 중복 시 에러 발생
            )
            return len(created)

    @staticmethod
    def get_budget_stats() -> Dict:
        """
        예산 통계 조회

        Returns:
            Dict: 예산 통계
                {
                    'total_budget': int,
                    'total_execution': int,
                    'execution_rate': float
                }
        """
        from django.db.models import Max

        # 과제별로 total_budget의 최대값(실제로는 동일한 값) 합산
        project_budgets = ResearchProject.objects.values('project_number').annotate(
            budget=Max('total_budget')
        ).aggregate(
            total=Sum('budget')
        )

        total_budget = project_budgets['total'] or 0

        # 집행 완료된 금액의 합계
        execution_stats = ResearchProject.objects.filter(
            status='집행완료'
        ).aggregate(
            total_execution=Sum('execution_amount')
        )

        total_execution = execution_stats['total_execution'] or 0

        # 집행률 계산
        execution_rate = (total_execution / total_budget * 100) if total_budget > 0 else 0

        return {
            'total_budget': total_budget,
            'total_execution': total_execution,
            'execution_rate': round(execution_rate, 2)
        }

    @staticmethod
    def get_by_item() -> List[Dict]:
        """
        집행 항목별 금액 조회

        Returns:
            List[Dict]: 집행 항목별 데이터
                [
                    {
                        'execution_item': '연구장비 도입',
                        'total_amount': 150000000
                    },
                    ...
                ]
        """
        result = ResearchProject.objects.values('execution_item').annotate(
            total_amount=Coalesce(Sum('execution_amount'), Value(0))
        ).order_by('-total_amount')

        return list(result)

    @staticmethod
    def get_by_agency() -> List[Dict]:
        """
        지원 기관별 예산 조회

        Returns:
            List[Dict]: 지원 기관별 데이터
                [
                    {
                        'funding_agency': '한국연구재단',
                        'total_budget': 500000000
                    },
                    ...
                ]
        """
        from django.db.models import Max, Sum as DbSum

        # 과제별로 total_budget을 먼저 가져온 후, 기관별로 합산
        # Step 1: 각 과제번호별로 total_budget의 최대값 (모든 집행 내역은 동일한 total_budget을 가짐)
        projects_by_agency = ResearchProject.objects.values(
            'funding_agency', 'project_number'
        ).annotate(
            project_budget=Max('total_budget')
        )

        # Step 2: 기관별로 과제 예산 합산
        from collections import defaultdict
        agency_budgets = defaultdict(int)

        for project in projects_by_agency:
            agency_budgets[project['funding_agency']] += project['project_budget']

        # Step 3: 결과를 정렬하여 반환
        result = [
            {
                'funding_agency': agency,
                'total_budget': total
            }
            for agency, total in sorted(
                agency_budgets.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]

        return result

    @staticmethod
    def delete_by_execution_ids(execution_ids: List[str]) -> int:
        """
        집행 ID 목록으로 삭제

        Args:
            execution_ids: 집행 ID 리스트

        Returns:
            int: 삭제된 행 수
        """
        deleted_count, _ = ResearchProject.objects.filter(
            execution_id__in=execution_ids
        ).delete()

        return deleted_count
