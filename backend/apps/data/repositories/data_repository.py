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
from apps.dashboard.persistence.models import DepartmentKPI, Publication, ResearchProject, Student


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
            obj = model_class.objects.get(id=obj_id)
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

        if data_type is None or data_type == DataType.DEPARTMENT_KPI:
            querysets.append((
                DataType.DEPARTMENT_KPI,
                DepartmentKPI.objects.all()
            ))

        if data_type is None or data_type == DataType.PUBLICATION:
            querysets.append((
                DataType.PUBLICATION,
                Publication.objects.all()
            ))

        if data_type is None or data_type == DataType.RESEARCH_PROJECT:
            querysets.append((
                DataType.RESEARCH_PROJECT,
                ResearchProject.objects.all()
            ))

        if data_type is None or data_type == DataType.STUDENT_ROSTER:
            querysets.append((
                DataType.STUDENT_ROSTER,
                Student.objects.all()
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
            if data_type == DataType.DEPARTMENT_KPI:
                queryset = queryset.filter(evaluation_year=filters.year)
            elif data_type == DataType.PUBLICATION:
                queryset = queryset.filter(publication_date__year=filters.year)
            elif data_type == DataType.RESEARCH_PROJECT:
                queryset = queryset.filter(execution_date__year=filters.year)
            elif data_type == DataType.STUDENT_ROSTER:
                queryset = queryset.filter(admission_year=filters.year)

        # 검색어 필터 (2자 이상, 설계 문서 BR-201 기준)
        if filters.search and len(filters.search) >= 2:
            search_q = Q()
            if data_type == DataType.DEPARTMENT_KPI:
                # 단과대학, 학과
                search_q |= Q(college__icontains=filters.search)
                search_q |= Q(department__icontains=filters.search)
            elif data_type == DataType.PUBLICATION:
                # 논문제목, 주저자, 참여저자, 학술지명
                search_q |= Q(paper_title__icontains=filters.search)
                search_q |= Q(lead_author__icontains=filters.search)
                search_q |= Q(co_authors__icontains=filters.search)
                search_q |= Q(journal_name__icontains=filters.search)
            elif data_type == DataType.RESEARCH_PROJECT:
                # 과제번호, 과제명, 연구책임자
                search_q |= Q(project_number__icontains=filters.search)
                search_q |= Q(project_name__icontains=filters.search)
                search_q |= Q(principal_investigator__icontains=filters.search)
            elif data_type == DataType.STUDENT_ROSTER:
                # 이름, 학과, 지도교수, 이메일
                search_q |= Q(name__icontains=filters.search)
                search_q |= Q(department__icontains=filters.search)
                search_q |= Q(advisor__icontains=filters.search)
                search_q |= Q(email__icontains=filters.search)

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
            DataType.DEPARTMENT_KPI: DepartmentKPI,
            DataType.PUBLICATION: Publication,
            DataType.RESEARCH_PROJECT: ResearchProject,
            DataType.STUDENT_ROSTER: Student,
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
        # uploaded_by는 현재 모델에 없으므로 임시로 시스템 사용자로 설정
        # TODO: 향후 uploaded_by ForeignKey 추가 후 수정
        uploaded_by_email = "system@university.ac.kr"

        if data_type == DataType.DEPARTMENT_KPI:
            return UnifiedDataItem(
                id=obj.id,
                data_type=data_type,
                date=obj.created_at.date(),  # 평가년도는 extra_fields에
                title=f"{obj.evaluation_year}년 {obj.department}",
                uploaded_at=obj.created_at,
                uploaded_by=uploaded_by_email,
                amount=obj.tech_transfer_income,  # 기술이전 수입액
                category=obj.college,
                description=None,
                extra_fields={
                    "evaluation_year": obj.evaluation_year,
                    "department": obj.department,
                    "employment_rate": float(obj.employment_rate),
                    "full_time_faculty": obj.full_time_faculty,
                    "visiting_faculty": obj.visiting_faculty,
                    "tech_transfer_income": float(obj.tech_transfer_income),
                    "intl_conferences": obj.intl_conferences,
                }
            )

        elif data_type == DataType.PUBLICATION:
            return UnifiedDataItem(
                id=obj.id,
                data_type=data_type,
                date=obj.publication_date,
                title=obj.paper_title,
                uploaded_at=obj.created_at,
                uploaded_by=uploaded_by_email,
                category=obj.department,
                description=None,
                extra_fields={
                    "paper_id": obj.paper_id,
                    "college": obj.college,
                    "lead_author": obj.lead_author,
                    "co_authors": obj.co_authors or "",
                    "journal_name": obj.journal_name,
                    "journal_grade": obj.journal_grade,
                    "impact_factor": float(obj.impact_factor) if obj.impact_factor else None,
                    "project_linked": obj.project_linked,
                }
            )

        elif data_type == DataType.RESEARCH_PROJECT:
            return UnifiedDataItem(
                id=obj.id,
                data_type=data_type,
                date=obj.execution_date,
                title=obj.project_name,
                uploaded_at=obj.created_at,
                uploaded_by=uploaded_by_email,
                amount=obj.execution_amount,  # 집행금액
                category=obj.department,
                description=obj.remarks or "",
                extra_fields={
                    "execution_id": obj.execution_id,
                    "project_number": obj.project_number,
                    "principal_investigator": obj.principal_investigator,
                    "funding_agency": obj.funding_agency,
                    "total_budget": obj.total_budget,
                    "execution_item": obj.execution_item,
                    "execution_amount": obj.execution_amount,
                    "status": obj.status,
                }
            )

        elif data_type == DataType.STUDENT_ROSTER:
            # Student는 날짜가 없으므로 created_at 사용
            return UnifiedDataItem(
                id=obj.id,
                data_type=data_type,
                date=obj.created_at.date(),  # datetime을 date로 변환
                title=obj.name,
                uploaded_at=obj.created_at,
                uploaded_by=uploaded_by_email,
                category=obj.department,
                description=None,
                extra_fields={
                    "student_id": obj.student_id,
                    "college": obj.college,
                    "grade": obj.grade,
                    "program_type": obj.program_type,
                    "enrollment_status": obj.enrollment_status,
                    "gender": obj.gender,
                    "admission_year": obj.admission_year,
                    "advisor": obj.advisor or "",
                    "email": obj.email,
                }
            )

        else:
            raise ValueError(f"Unknown data_type: {data_type}")
