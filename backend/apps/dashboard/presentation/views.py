# -*- coding: utf-8 -*-
"""
Dashboard Views

API 엔드포인트
"""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime

from infrastructure.authentication.supabase_auth import SupabaseAuthentication
from apps.dashboard.services.dashboard_service import DashboardService
from apps.dashboard.presentation.serializers import (
    DashboardResponseSerializer,
    FilterParamsSerializer
)


class DashboardViewSet(viewsets.ViewSet):
    """
    대시보드 ViewSet

    GET /api/dashboard/ - 대시보드 데이터 조회
    """
    authentication_classes = [SupabaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dashboard_service = DashboardService()

    def list(self, request):
        """
        GET /api/dashboard/
        대시보드 데이터 조회

        Query Parameters:
            - year (int, optional): 조회할 연도 (기본값: 현재 연도)
            - department (str, optional): 부서명 (기본값: 'all')

        Returns:
            200 OK: 대시보드 데이터
            400 Bad Request: 잘못된 파라미터
            401 Unauthorized: 인증 필요
            500 Internal Server Error: 서버 오류
        """
        # 쿼리 파라미터 검증
        filter_serializer = FilterParamsSerializer(data=request.query_params)
        if not filter_serializer.is_valid():
            return Response(
                filter_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        year = filter_serializer.validated_data.get('year', datetime.now().year)
        department = filter_serializer.validated_data.get('department', 'all')

        try:
            # 서비스 호출
            dashboard_data = self.dashboard_service.get_dashboard_data(year, department)

            # 응답 직렬화
            response_serializer = DashboardResponseSerializer(dashboard_data)

            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # 에러 로깅 (실제로는 StructuredLogger 사용)
            print(f"Dashboard error: {str(e)}")

            return Response(
                {'error': '데이터를 불러오는 중 오류가 발생했습니다'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
