# -*- coding: utf-8 -*-
"""
Paper Repository

논문 데이터 접근 계층
"""
from typing import List
from django.db.models import Count

from apps.core.repositories.base_repository import BaseRepository
from apps.dashboard.persistence.models import Paper as PaperORM
from apps.dashboard.domain.models import Paper, PaperCount


class PaperRepository(BaseRepository):
    """
    논문 Repository

    ORM 쿼리를 도메인 모델로 변환합니다.
    """
    model = PaperORM

    def get_count_by_year(self, year: int, department: str = 'all') -> int:
        """
        연도별 논문 수 조회

        Args:
            year: 조회할 연도
            department: 부서명 (기본값: 'all')

        Returns:
            int: 논문 수
        """
        queryset = self.model.objects.filter(
            is_deleted=False,
            publication_date__year=year
        )

        # if department != 'all':
        #     queryset = queryset.filter(department=department)

        return queryset.count()

    def get_distribution_by_category(self, year: int, department: str = 'all') -> List[PaperCount]:
        """
        카테고리별 논문 분포 조회

        Args:
            year: 조회할 연도
            department: 부서명 (기본값: 'all')

        Returns:
            List[PaperCount]: 카테고리별 논문 수 리스트
        """
        queryset = self.model.objects.filter(
            is_deleted=False,
            publication_date__year=year
        )

        # if department != 'all':
        #     queryset = queryset.filter(department=department)

        # 카테고리별 집계 (field를 category로 사용)
        distribution = queryset.values('field').annotate(
            count=Count('id')
        ).order_by('-count')

        return [
            PaperCount(
                category=item['field'],
                count=item['count']
            )
            for item in distribution
        ]

    def get_all_by_year(self, year: int, department: str = 'all') -> List[Paper]:
        """
        연도별 논문 전체 조회

        Args:
            year: 조회할 연도
            department: 부서명 (기본값: 'all')

        Returns:
            List[Paper]: 논문 리스트
        """
        queryset = self.model.objects.filter(
            is_deleted=False,
            publication_date__year=year
        )

        # if department != 'all':
        #     queryset = queryset.filter(department=department)

        papers = queryset.order_by('-publication_date')

        return [self._to_domain(paper) for paper in papers]

    def _to_domain(self, orm_obj: PaperORM) -> Paper:
        """ORM 모델 → 도메인 모델 변환"""
        return Paper(
            id=orm_obj.id,
            category=orm_obj.field
        )

    def bulk_create(self, papers: List[dict], user_id: str) -> int:
        """
        논문 데이터 배치 생성

        Args:
            papers: 논문 데이터 리스트 (파싱된 딕셔너리)
            user_id: 업로드한 사용자 ID

        Returns:
            int: 생성된 행 수
        """
        from apps.accounts.persistence.models import UserProfile

        user = UserProfile.objects.get(id=user_id)

        paper_objs = [
            PaperORM(
                title=paper['title'],
                authors=paper['authors'],
                publication_date=paper['publication_date'],
                field=paper['field'],
                journal_name=paper.get('journal_name', paper.get('저널명', '')),
                doi=paper.get('doi', paper.get('DOI', '')),
                uploaded_by=user
            )
            for paper in papers
        ]

        PaperORM.objects.bulk_create(paper_objs)
        return len(paper_objs)

    def check_duplicates(self, papers: List[dict]) -> List[dict]:
        """
        중복 데이터 확인

        Args:
            papers: 논문 데이터 리스트

        Returns:
            List[dict]: 중복된 데이터 리스트
        """
        duplicates = []

        for paper in papers:
            exists = PaperORM.objects.filter(
                title=paper['title'],
                publication_date=paper['publication_date'],
                is_deleted=False
            ).exists()

            if exists:
                duplicates.append(paper)

        return duplicates

    def _to_orm(self, domain_obj: Paper) -> PaperORM:
        """도메인 모델 → ORM 모델 변환"""
        # 이 메서드는 create/update 시 사용
        pass
