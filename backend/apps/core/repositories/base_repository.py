# -*- coding: utf-8 -*-
"""
Base Repository

책임:
- 공통 CRUD 메서드 제공
- ORM 쿼리 추상화
- 도메인 모델 ↔ ORM 모델 변환
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from django.db.models import Model, QuerySet


class BaseRepository(ABC):
    """
    기본 Repository 추상 클래스

    하위 클래스에서 model 속성을 반드시 정의해야 합니다.
    """

    model: Model = None  # 하위 클래스에서 ORM 모델 지정

    def get_by_id(self, id: int) -> Optional[Any]:
        """
        ID로 단일 객체 조회

        Args:
            id: 객체 ID

        Returns:
            도메인 모델 객체 또는 None
        """
        try:
            orm_obj = self.model.objects.get(id=id)
            return self._to_domain(orm_obj)
        except self.model.DoesNotExist:
            return None

    def get_all(self, filters: Dict[str, Any] = None) -> List[Any]:
        """
        전체 또는 필터링된 객체 목록 조회

        Args:
            filters: 필터 조건 딕셔너리

        Returns:
            도메인 모델 객체 리스트
        """
        queryset = self.model.objects.all()

        if filters:
            queryset = queryset.filter(**filters)

        return [self._to_domain(orm_obj) for orm_obj in queryset]

    def create(self, data: Dict[str, Any]) -> Any:
        """
        새 객체 생성

        Args:
            data: 생성할 데이터

        Returns:
            생성된 도메인 모델 객체
        """
        orm_obj = self.model.objects.create(**data)
        return self._to_domain(orm_obj)

    def bulk_create(self, data_list: List[Dict[str, Any]]) -> List[Any]:
        """
        여러 객체 일괄 생성

        Args:
            data_list: 생성할 데이터 리스트

        Returns:
            생성된 도메인 모델 객체 리스트
        """
        orm_objs = [self.model(**data) for data in data_list]
        created_objs = self.model.objects.bulk_create(orm_objs)
        return [self._to_domain(orm_obj) for orm_obj in created_objs]

    def update(self, id: int, data: Dict[str, Any]) -> Optional[Any]:
        """
        객체 업데이트

        Args:
            id: 객체 ID
            data: 업데이트할 데이터

        Returns:
            업데이트된 도메인 모델 객체 또는 None
        """
        try:
            orm_obj = self.model.objects.get(id=id)
            for key, value in data.items():
                setattr(orm_obj, key, value)
            orm_obj.save()
            return self._to_domain(orm_obj)
        except self.model.DoesNotExist:
            return None

    def delete(self, id: int) -> bool:
        """
        객체 삭제 (하드 삭제)

        Args:
            id: 객체 ID

        Returns:
            삭제 성공 여부
        """
        try:
            orm_obj = self.model.objects.get(id=id)
            orm_obj.delete()
            return True
        except self.model.DoesNotExist:
            return False

    def count(self, filters: Dict[str, Any] = None) -> int:
        """
        객체 개수 조회

        Args:
            filters: 필터 조건 딕셔너리

        Returns:
            객체 개수
        """
        queryset = self.model.objects.all()

        if filters:
            queryset = queryset.filter(**filters)

        return queryset.count()

    @abstractmethod
    def _to_domain(self, orm_obj: Model) -> Any:
        """
        ORM 모델 → 도메인 모델 변환

        Args:
            orm_obj: ORM 모델 객체

        Returns:
            도메인 모델 객체
        """
        pass

    @abstractmethod
    def _to_orm(self, domain_obj: Any) -> Model:
        """
        도메인 모델 → ORM 모델 변환

        Args:
            domain_obj: 도메인 모델 객체

        Returns:
            ORM 모델 객체
        """
        pass
