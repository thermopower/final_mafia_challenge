# -*- coding: utf-8 -*-
"""
Publication Repository

논문 데이터 접근 계층
"""
from typing import List, Dict, Optional
from decimal import Decimal
from django.db.models import Count, Avg, Q, Value
from django.db.models.functions import Coalesce, ExtractYear
from django.db import transaction

from apps.dashboard.persistence.models import Publication


class PublicationRepository:
    """
    논문 데이터 Repository

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
                        'paper_id': 'PUB-24-001',
                        'publication_date': date(2024, 3, 15),
                        'college': '공과대학',
                        'department': '컴퓨터공학과',
                        'paper_title': 'Deep Learning in Network Security',
                        'lead_author': '김민준',
                        'co_authors': '박지훈;최민서',
                        'journal_name': 'IEEE Transactions on Computers',
                        'journal_grade': 'SCIE',
                        'impact_factor': Decimal('3.45'),
                        'project_linked': 'Y'
                    },
                    ...
                ]

        Returns:
            int: 삽입된 행 수
        """
        if not data_list:
            return 0

        with transaction.atomic():
            objects = [Publication(**data) for data in data_list]
            created = Publication.objects.bulk_create(
                objects,
                ignore_conflicts=False  # 중복 시 에러 발생
            )
            return len(created)

    @staticmethod
    def get_count_by_period(year: Optional[int] = None) -> Dict:
        """
        기간별 논문 통계 조회

        Args:
            year: 연도 (None이면 전체)

        Returns:
            Dict: 논문 통계
                {
                    'total_papers': int,
                    'scie_count': int,
                    'kci_count': int,
                    'avg_impact_factor': Decimal,
                    'project_linked_count': int
                }
        """
        queryset = Publication.objects.all()

        if year:
            queryset = queryset.filter(publication_date__year=year)

        total_papers = queryset.count()
        scie_count = queryset.filter(journal_grade='SCIE').count()
        kci_count = queryset.filter(journal_grade='KCI').count()

        # SCIE 논문의 평균 Impact Factor
        scie_papers = queryset.filter(
            journal_grade='SCIE',
            impact_factor__isnull=False
        )
        avg_impact_factor = scie_papers.aggregate(
            avg=Avg('impact_factor')
        )['avg'] or Decimal('0')

        project_linked_count = queryset.filter(project_linked='Y').count()

        return {
            'total_papers': total_papers,
            'scie_count': scie_count,
            'kci_count': kci_count,
            'avg_impact_factor': avg_impact_factor,
            'project_linked_count': project_linked_count
        }

    @staticmethod
    def get_by_department(year: Optional[int] = None) -> List[Dict]:
        """
        학과별 논문 수 조회

        Args:
            year: 연도 (None이면 전체)

        Returns:
            List[Dict]: 학과별 데이터
                [
                    {
                        'department': '컴퓨터공학과',
                        'count': 10
                    },
                    ...
                ]
        """
        queryset = Publication.objects.all()

        if year:
            queryset = queryset.filter(publication_date__year=year)

        result = queryset.values('department').annotate(
            count=Count('id')
        ).order_by('-count')

        return list(result)

    @staticmethod
    def get_grade_distribution(year: Optional[int] = None) -> List[Dict]:
        """
        저널 등급별 논문 분포 조회 (파이 차트용)

        Args:
            year: 연도 (None이면 전체)

        Returns:
            List[Dict]: 저널 등급별 데이터
                [
                    {
                        'journal_grade': 'SCIE',
                        'count': 30
                    },
                    ...
                ]
        """
        queryset = Publication.objects.all()

        if year:
            queryset = queryset.filter(publication_date__year=year)

        result = queryset.values('journal_grade').annotate(
            count=Count('id')
        ).order_by('journal_grade')

        return list(result)

    @staticmethod
    def delete_by_paper_ids(paper_ids: List[str]) -> int:
        """
        논문 ID 목록으로 삭제

        Args:
            paper_ids: 논문 ID 리스트

        Returns:
            int: 삭제된 행 수
        """
        deleted_count, _ = Publication.objects.filter(
            paper_id__in=paper_ids
        ).delete()

        return deleted_count
