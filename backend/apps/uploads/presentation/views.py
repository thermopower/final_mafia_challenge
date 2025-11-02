# -*- coding: utf-8 -*-
"""
Upload API Views

CSV 파일 업로드 API 엔드포인트
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny  # 인증 없이 접근 허용

from apps.uploads.presentation.serializers import FileUploadSerializer
from apps.uploads.services.file_processor import FileProcessorService


class FileUploadView(APIView):
    """
    CSV 파일 업로드 API

    POST /api/uploads/
        - 4가지 타입의 CSV 파일 업로드
        - 파싱, 검증, DB 저장까지 수행

    Note: 개발 환경에서는 인증 없이 테스트 가능하도록 AllowAny 설정
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]  # 👈 개발용: 인증 없이 접근 허용

    def post(self, request):
        """
        CSV 파일 업로드

        Args:
            request: HTTP 요청
                - file: CSV 파일
                - data_type: 데이터 유형

        Returns:
            Response: 업로드 결과
        """
        # 1. 요청 검증
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. 파일 처리
        file = serializer.validated_data['file']
        data_type = serializer.validated_data['data_type']

        try:
            processor = FileProcessorService()
            result = processor.process_file(file, data_type)

            # 3. 검증 실패 시
            if not result['success']:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            # 4. 성공 응답
            return Response(result, status=status.HTTP_200_OK)

        except ValueError as e:
            # 파일 형식 오류 등
            return Response(
                {
                    'success': False,
                    'errors': [str(e)]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            # 예상치 못한 오류
            return Response(
                {
                    'success': False,
                    'errors': [f"업로드 중 오류가 발생했습니다: {str(e)}"]
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
