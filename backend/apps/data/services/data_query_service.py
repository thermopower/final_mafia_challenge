# -*- coding: utf-8 -*-
"""
DataQueryService

데이터 조회 및 필터링 비즈니스 로직을 담당합니다.
"""

from typing import Optional

from apps.data.domain.models import DataType, DataFilter, PaginatedDataResult, UnifiedDataItem
from apps.data.repositories.data_repository import DataRepository


class DataQueryService:
    """
    데이터 조회 서비스

    Responsibility:
    - 데이터 필터링 및 조회 비즈니스 로직
    - Repository 계층과 Presentation 계층 사이의 중개
    """

    def __init__(self, data_repository: Optional[DataRepository] = None):
        """
        Args:
            data_repository: DataRepository 인스턴스 (의존성 주입)
        """
        self.data_repository = data_repository or DataRepository()

    def get_filtered_data(
        self,
        filters: DataFilter,
        page: int,
        page_size: int
    ) -> PaginatedDataResult:
        """
        필터 조건에 맞는 데이터를 페이지네이션하여 조회

        Args:
            filters: 필터 조건
            page: 페이지 번호
            page_size: 페이지 크기

        Returns:
            PaginatedDataResult: 페이지네이션 결과
        """
        # Repository에 위임
        return self.data_repository.get_all_with_filters(filters, page, page_size)

    def get_data_by_id(
        self,
        data_type: DataType,
        obj_id: int
    ) -> Optional[UnifiedDataItem]:
        """
        데이터 유형과 ID로 단일 데이터 조회

        Args:
            data_type: 데이터 유형
            obj_id: 객체 ID

        Returns:
            UnifiedDataItem 또는 None
        """
        return self.data_repository.get_by_id(data_type, obj_id)
