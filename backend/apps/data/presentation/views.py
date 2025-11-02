# -*- coding: utf-8 -*-
"""
Data API Views
"""

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.data.domain.models import DataType, DataFilter
from apps.data.services.data_query_service import DataQueryService
from apps.data.services.csv_export_service import CSVExportService
from apps.data.presentation.serializers import PaginatedDataResponseSerializer


class DataListView(APIView):
    """
    데이터 목록 조회 API

    GET /api/data/
    Query Parameters:
        - page: int (기본값: 1)
        - page_size: int (기본값: 20, 허용값: 20/50/100)
        - ordering: str (기본값: -date, 허용값: date/-date/amount/-amount)
        - type: str (optional, 예: department_kpi/publication/research_project/student_roster)
        - year: int (optional)
        - search: str (optional, 최소 2자)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = DataQueryService()

    def get(self, request):
        """데이터 목록 조회"""
        # 1. 쿼리 파라미터 파싱
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        ordering = request.query_params.get('ordering', '-date')
        data_type_str = request.query_params.get('type', None)
        year = request.query_params.get('year', None)
        search = request.query_params.get('search', None)

        # 2. 데이터 유형 변환
        data_type = None
        if data_type_str:
            try:
                data_type = DataType(data_type_str)
            except ValueError:
                return Response(
                    {"error": f"Invalid data_type: {data_type_str}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # 3. 필터 객체 생성
        filters = DataFilter(
            data_type=data_type,
            year=int(year) if year else None,
            search=search,
            ordering=ordering
        )

        # 4. 서비스 호출
        result = self.service.get_filtered_data(filters, page, page_size)

        # 5. 직렬화 및 응답
        serializer = PaginatedDataResponseSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DataDetailView(APIView):
    """
    데이터 상세 조회 API

    GET /api/data/<type>/<id>/
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = DataQueryService()

    def get(self, request, data_type: str, pk: int):
        """데이터 상세 조회"""
        # 1. 데이터 유형 변환
        try:
            data_type_enum = DataType(data_type)
        except ValueError:
            return Response(
                {"error": f"Invalid data_type: {data_type}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. 서비스 호출
        item = self.service.get_data_by_id(data_type_enum, pk)

        if item is None:
            return Response(
                {"error": "Data not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. 직렬화 및 응답
        return Response(item.to_dict(), status=status.HTTP_200_OK)


class ExportView(APIView):
    """
    CSV 내보내기 API

    GET /api/data/export/
    Query Parameters:
        - type: str (optional, 예: department_kpi/publication/research_project/student_roster)
        - year: int (optional)
        - search: str (optional, 최소 2자)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CSVExportService()

    def get(self, request):
        """CSV 데이터 내보내기"""
        # 1. 쿼리 파라미터 파싱
        data_type_str = request.query_params.get('type', None)
        year = request.query_params.get('year', None)
        search = request.query_params.get('search', None)

        # 2. 데이터 유형 변환
        data_type = None
        if data_type_str:
            try:
                data_type = DataType(data_type_str)
            except ValueError:
                return Response(
                    {"error": f"Invalid data_type: {data_type_str}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # 3. 필터 객체 생성
        filters = DataFilter(
            data_type=data_type,
            year=int(year) if year else None,
            search=search,
            ordering="-date"  # CSV는 기본 정렬
        )

        # 4. CSV 생성
        csv_content = self.service.export_to_csv(filters)

        # 5. 파일명 생성
        # 데이터 유형이 지정되지 않았으면 기본값 사용
        filename = self.service.generate_filename(
            data_type if data_type else DataType.DEPARTMENT_KPI
        )

        # 6. HttpResponse로 CSV 반환
        response = HttpResponse(
            csv_content.encode('utf-8-sig'),
            content_type='text/csv; charset=utf-8-sig'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
