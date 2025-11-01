# -*- coding: utf-8 -*-
"""
Upload Views

Excel 파일 업로드 및 이력 조회 API
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from infrastructure.permissions.admin_permission import IsAdmin
from apps.uploads.presentation.serializers import (
    ExcelUploadSerializer,
    UploadRecordSerializer,
)
from apps.uploads.repositories.upload_repository import UploadRepository
from apps.uploads.services.file_processor import FileProcessorService
from apps.core.exceptions import ValidationError
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class ExcelUploadViewSet(viewsets.ViewSet):
    """Excel 업로드 ViewSet"""

    permission_classes = [IsAuthenticated, IsAdmin]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.upload_repo = UploadRepository()
        self.file_processor = FileProcessorService()

    @action(detail=False, methods=["post"], url_path="excel")
    def upload_excel(self, request):
        """
        Excel 파일 업로드

        Request (multipart/form-data):
          - file: Excel 파일
          - data_type: 데이터 유형 ('performance', 'paper', 'student', 'budget')

        Response 201 Created:
          - id: 업로드 ID
          - filename: 파일명
          - data_type: 데이터 유형
          - rows_processed: 처리된 행 수
          - uploaded_at: 업로드 일시
          - uploaded_by: 업로드 사용자
          - status: 상태 ('success', 'failed', 'partial')

        Response 400 Bad Request:
          - error: 오류 메시지
          - details: 오류 상세 정보

        Response 403 Forbidden:
          - error: "관리자만 접근할 수 있습니다"

        Response 500 Internal Server Error:
          - error: "업로드 중 오류가 발생했습니다"
        """
        # Serializer 검증
        serializer = ExcelUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = serializer.validated_data["file"]
        data_type = serializer.validated_data["data_type"]
        user_id = request.user.id

        try:
            # 파일 처리
            result = self.file_processor.process_file(file, data_type, str(user_id))

            # 성공 응답
            response_serializer = UploadRecordSerializer(result.upload_record)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # 검증 오류
            logger.warning(f"Validation error: {e.message}")
            return Response(
                {"error": e.message, "details": e.details},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            # 예상치 못한 오류
            logger.error(f"Unexpected error during upload: {str(e)}")
            return Response(
                {"error": "업로드 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], url_path="history")
    def get_history(self, request):
        """
        업로드 이력 조회

        Query Parameters:
          - page: 페이지 번호 (기본값: 1)
          - page_size: 페이지당 항목 수 (기본값: 20)

        Response 200 OK:
          - count: 전체 항목 수
          - next: 다음 페이지 URL
          - previous: 이전 페이지 URL
          - results: 업로드 레코드 리스트
        """
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))

        records, total_count = self.upload_repo.get_upload_history(page, page_size)
        serializer = UploadRecordSerializer(records, many=True)

        # Pagination 정보 생성
        next_page = page + 1 if (page * page_size) < total_count else None
        previous_page = page - 1 if page > 1 else None

        return Response(
            {
                "count": total_count,
                "next": (
                    f"/api/upload/history/?page={next_page}&page_size={page_size}"
                    if next_page
                    else None
                ),
                "previous": (
                    f"/api/upload/history/?page={previous_page}&page_size={page_size}"
                    if previous_page
                    else None
                ),
                "results": serializer.data,
            }
        )
