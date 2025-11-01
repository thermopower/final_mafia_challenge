# -*- coding: utf-8 -*-
"""
Export View Tests
"""

import pytest
from unittest.mock import Mock, patch
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.data.domain.models import DataType

User = get_user_model()


class TestExportView:
    """ExportView API 테스트"""

    @pytest.fixture
    def api_client(self, db):
        """인증된 API 클라이언트 fixture"""
        # 테스트 사용자 생성
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    @pytest.fixture
    def mock_csv_service(self):
        """Mock CSV Export Service"""
        with patch('apps.data.presentation.views.CSVExportService') as mock:
            service_instance = Mock()
            service_instance.export_to_csv.return_value = '\ufeff날짜,항목,금액,카테고리,설명\n'
            service_instance.generate_filename.return_value = 'performance_20241101_120000.csv'
            mock.return_value = service_instance
            yield service_instance

    def test_export_csv_with_default_filters(self, api_client, mock_csv_service):
        """기본 필터로 CSV 내보내기 테스트"""
        # Arrange
        url = '/api/data/export/'

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/csv; charset=utf-8-sig'
        assert 'Content-Disposition' in response
        assert 'attachment; filename=' in response['Content-Disposition']
        # BOM 확인
        assert response.content.startswith(b'\xef\xbb\xbf')

    def test_export_csv_with_data_type_filter(self, api_client, mock_csv_service):
        """데이터 유형 필터로 CSV 내보내기"""
        # Arrange
        url = '/api/data/export/?type=performance'

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert 'performance_' in response['Content-Disposition']
        # UTF-8 BOM 확인
        assert response.content.startswith(b'\xef\xbb\xbf')

    def test_export_csv_with_year_filter(self, api_client, mock_csv_service):
        """연도 필터로 CSV 내보내기"""
        # Arrange
        url = '/api/data/export/?type=paper&year=2024'
        mock_csv_service.generate_filename.return_value = 'paper_20241101_120000.csv'

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert 'paper_' in response['Content-Disposition']

    def test_export_csv_with_search_filter(self, api_client, mock_csv_service):
        """검색어 필터로 CSV 내보내기"""
        # Arrange
        url = '/api/data/export/?type=student&search=김철수'
        mock_csv_service.generate_filename.return_value = 'student_20241101_120000.csv'

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert 'student_' in response['Content-Disposition']

    def test_export_csv_with_invalid_data_type(self, api_client, mock_csv_service):
        """잘못된 데이터 유형으로 요청 시 에러"""
        # Arrange
        url = '/api/data/export/?type=invalid'

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.json()

    def test_export_csv_filename_format(self, api_client, mock_csv_service):
        """CSV 파일명 형식 검증 (data_type_YYYYMMDD_HHMMSS.csv)"""
        # Arrange
        url = '/api/data/export/?type=budget'
        mock_csv_service.generate_filename.return_value = 'budget_20241101_120000.csv'

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        content_disposition = response['Content-Disposition']
        # 파일명 형식 확인: budget_YYYYMMDD_HHMMSS.csv
        assert 'budget_' in content_disposition
        assert '.csv' in content_disposition
        # 타임스탬프 형식 확인 (8자리 날짜 + _ + 6자리 시간)
        import re
        pattern = r'budget_\d{8}_\d{6}\.csv'
        assert re.search(pattern, content_disposition)

    def test_export_csv_headers_for_performance(self, api_client, mock_csv_service):
        """Performance 데이터 유형의 CSV 헤더 검증"""
        # Arrange
        url = '/api/data/export/?type=performance'

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        csv_content = response.content.decode('utf-8-sig')
        lines = csv_content.split('\n')
        # 첫 번째 줄이 헤더
        assert '날짜' in lines[0]
        assert '항목' in lines[0]
        assert '금액' in lines[0]
        assert '카테고리' in lines[0]
        assert '설명' in lines[0]
