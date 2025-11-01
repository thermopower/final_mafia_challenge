# -*- coding: utf-8 -*-
"""
DataRepository

모든 데이터 유형(Performance, Paper, Student, Budget)을 통합하여 조회하는 Repository입니다.
"""

from typing import Optional, List
from decimal import Decimal
from datetime import date

from django.db.models import Q, QuerySet
from django.core.paginator import Paginator

from apps.data.domain.models import DataType, DataFilter, UnifiedDataItem, PaginatedDataResult
from apps.dashboard.persistence.models import Performance, Paper, Student, Budget


class DataRepository:
    """
    데이터 통합 조회 Repository

    Responsibility:
    - 모든 데이터 유형을 통합하여 조회
    - 필터링, 정렬, 페이지네이션 적용
    - ORM 모델을 도메인 모델로 변환
    """

    def get_all_with_filters(
        self,
        filters: DataFilter,
        page: int = 1,
        page_size: int = 20
    ) -> PaginatedDataResult:
        """
        필터 조건에 맞는 데이터를 페이지네이션하여 조회

        Args:
            filters: 필터 조건 (data_type, year, search, ordering)
            page: 페이지 번호 (1부터 시작)
            page_size: 페이지 크기 (기본값: 20)

        Returns:
            PaginatedDataResult: 페이지네이션 결과
        """
        # 1. 데이터 유형별로 QuerySet 가져오기
        querysets = self._get_querysets_by_type(filters.data_type)

        # 2. 각 QuerySet에 필터 적용
        filtered_querysets = []
        for data_type, queryset in querysets:
            filtered_qs = self._apply_filters(queryset, data_type, filters)
            filtered_querysets.append((data_type, filtered_qs))

        # 3. 모든 QuerySet을 UnifiedDataItem으로 변환
        all_items: List[UnifiedDataItem] = []
        for data_type, queryset in filtered_querysets:
            items = [self._to_domain(obj, data_type) for obj in queryset]
            all_items.extend(items)

        # 4. 정렬 적용
        all_items = self._apply_ordering(all_items, filters.ordering)

        # 5. 페이지네이션 적용
        total_count = len(all_items)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_items = all_items[start_index:end_index]

        # 6. next/previous URL 생성 (간단한 구현)
        has_next = end_index < total_count
        has_previous = page > 1
        next_url = f"?page={page + 1}" if has_next else None
        previous_url = f"?page={page - 1}" if has_previous else None

        return PaginatedDataResult(
            count=total_count,
            next=next_url,
            previous=previous_url,
            results=paginated_items
        )

    def get_by_id(self, data_type: DataType, obj_id: int) -> Optional[UnifiedDataItem]:
        """
        데이터 유형과 ID로 단일 데이터 조회

        Args:
            data_type: 데이터 유형
            obj_id: 객체 ID

        Returns:
            UnifiedDataItem 또는 None
        """
        model_class = self._get_model_class(data_type)
        try:
            obj = model_class.objects.get(id=obj_id, is_deleted=False)
            return self._to_domain(obj, data_type)
        except model_class.DoesNotExist:
            return None

    def get_all_without_pagination(self, filters: DataFilter) -> List[UnifiedDataItem]:
        """
        필터 조건에 맞는 모든 데이터를 조회 (페이지네이션 없음)

        CSV 내보내기 등에서 사용됩니다.

        Args:
            filters: 필터 조건

        Returns:
            UnifiedDataItem 리스트
        """
        # 1. 데이터 유형별로 QuerySet 가져오기
        querysets = self._get_querysets_by_type(filters.data_type)

        # 2. 각 QuerySet에 필터 적용
        filtered_querysets = []
        for data_type, queryset in querysets:
            filtered_qs = self._apply_filters(queryset, data_type, filters)
            filtered_querysets.append((data_type, filtered_qs))

        # 3. 모든 QuerySet을 UnifiedDataItem으로 변환
        all_items: List[UnifiedDataItem] = []
        for data_type, queryset in filtered_querysets:
            items = [self._to_domain(obj, data_type) for obj in queryset]
            all_items.extend(items)

        # 4. 정렬 적용
        all_items = self._apply_ordering(all_items, filters.ordering)

        return all_items

    # ========== Private Methods ==========

    def _get_querysets_by_type(self, data_type: Optional[DataType] = None) -> List[tuple]:
        """
        데이터 유형별로 QuerySet을 가져옵니다.

        Args:
            data_type: 데이터 유형 (None이면 전체)

        Returns:
            List[(DataType, QuerySet)]
        """
        querysets = []

        if data_type is None or data_type == DataType.PERFORMANCE:
            querysets.append((
                DataType.PERFORMANCE,
                Performance.objects.filter(is_deleted=False).select_related('uploaded_by')
            ))

        if data_type is None or data_type == DataType.PAPER:
            querysets.append((
                DataType.PAPER,
                Paper.objects.filter(is_deleted=False).select_related('uploaded_by')
            ))

        if data_type is None or data_type == DataType.STUDENT:
            querysets.append((
                DataType.STUDENT,
                Student.objects.filter(is_deleted=False).select_related('uploaded_by')
            ))

        if data_type is None or data_type == DataType.BUDGET:
            querysets.append((
                DataType.BUDGET,
                Budget.objects.filter(is_deleted=False).select_related('uploaded_by')
            ))

        return querysets

    def _apply_filters(
        self,
        queryset: QuerySet,
        data_type: DataType,
        filters: DataFilter
    ) -> QuerySet:
        """
        QuerySet에 필터 조건 적용

        Args:
            queryset: 원본 QuerySet
            data_type: 데이터 유형
            filters: 필터 조건

        Returns:
            필터링된 QuerySet
        """
        # 연도 필터
        if filters.year:
            if data_type in [DataType.PERFORMANCE, DataType.PAPER]:
                date_field = 'date' if data_type == DataType.PERFORMANCE else 'publication_date'
                queryset = queryset.filter(**{f'{date_field}__year': filters.year})
            elif data_type == DataType.BUDGET:
                queryset = queryset.filter(fiscal_year=filters.year)
            # Student는 연도 필터가 없음

        # 검색어 필터 (title, description, category에서 부분 일치)
        if filters.search:
            search_q = Q()
            if data_type == DataType.PERFORMANCE:
                search_q |= Q(title__icontains=filters.search)
                search_q |= Q(description__icontains=filters.search)
                search_q |= Q(category__icontains=filters.search)
            elif data_type == DataType.PAPER:
                search_q |= Q(title__icontains=filters.search)
                search_q |= Q(authors__icontains=filters.search)
            elif data_type == DataType.STUDENT:
                search_q |= Q(name__icontains=filters.search)
                search_q |= Q(department__icontains=filters.search)
            elif data_type == DataType.BUDGET:
                search_q |= Q(item__icontains=filters.search)
                search_q |= Q(category__icontains=filters.search)

            queryset = queryset.filter(search_q)

        return queryset

    def _apply_ordering(
        self,
        items: List[UnifiedDataItem],
        ordering: str
    ) -> List[UnifiedDataItem]:
        """
        도메인 모델 리스트에 정렬 적용

        Args:
            items: UnifiedDataItem 리스트
            ordering: 정렬 기준 (예: '-date', 'amount')

        Returns:
            정렬된 리스트
        """
        reverse = ordering.startswith('-')
        order_field = ordering.lstrip('-')

        # 날짜 정렬
        if order_field == 'date':
            items.sort(key=lambda x: x.date, reverse=reverse)
        # 금액 정렬
        elif order_field == 'amount':
            items.sort(key=lambda x: x.amount or Decimal(0), reverse=reverse)
        # 제목 정렬
        elif order_field == 'title':
            items.sort(key=lambda x: x.title, reverse=reverse)

        return items

    def _get_model_class(self, data_type: DataType):
        """데이터 유형에 맞는 ORM 모델 클래스 반환"""
        mapping = {
            DataType.PERFORMANCE: Performance,
            DataType.PAPER: Paper,
            DataType.STUDENT: Student,
            DataType.BUDGET: Budget,
        }
        return mapping[data_type]

    def _to_domain(self, obj, data_type: DataType) -> UnifiedDataItem:
        """
        ORM 모델을 UnifiedDataItem 도메인 모델로 변환

        Args:
            obj: ORM 모델 인스턴스
            data_type: 데이터 유형

        Returns:
            UnifiedDataItem
        """
        if data_type == DataType.PERFORMANCE:
            return UnifiedDataItem(
                id=obj.id,
                data_type=data_type,
                date=obj.date,
                title=obj.title,
                uploaded_at=obj.created_at,
                uploaded_by=obj.uploaded_by.email,
                amount=obj.amount,
                category=obj.category,
                description=obj.description,
            )

        elif data_type == DataType.PAPER:
            return UnifiedDataItem(
                id=obj.id,
                data_type=data_type,
                date=obj.publication_date,
                title=obj.title,
                uploaded_at=obj.created_at,
                uploaded_by=obj.uploaded_by.email,
                category=obj.field,
                description=None,
                extra_fields={
                    "authors": obj.authors,
                    "journal_name": obj.journal_name,
                    "doi": obj.doi,
                }
            )

        elif data_type == DataType.STUDENT:
            # Student는 날짜가 없으므로 created_at 사용
            return UnifiedDataItem(
                id=obj.id,
                data_type=data_type,
                date=obj.created_at.date(),  # datetime을 date로 변환
                title=obj.name,
                uploaded_at=obj.created_at,
                uploaded_by=obj.uploaded_by.email,
                category=obj.department,
                description=None,
                extra_fields={
                    "student_id": obj.student_id,
                    "grade": obj.grade,
                    "status": obj.status,
                }
            )

        elif data_type == DataType.BUDGET:
            # Budget도 날짜가 없으므로 created_at 사용
            return UnifiedDataItem(
                id=obj.id,
                data_type=data_type,
                date=obj.created_at.date(),
                title=obj.item,
                uploaded_at=obj.created_at,
                uploaded_by=obj.uploaded_by.email,
                amount=obj.amount,
                category=obj.category,
                description=obj.description,
                extra_fields={
                    "fiscal_year": obj.fiscal_year,
                    "quarter": obj.quarter,
                }
            )

        else:
            raise ValueError(f"Unknown data_type: {data_type}")
