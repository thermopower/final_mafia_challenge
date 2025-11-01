# -*- coding: utf-8 -*-
"""
DataRepository 단위 테스트 (TDD Red Phase)

테스트를 먼저 작성한 후 구현합니다.
"""

import pytest
from datetime import date, datetime
from decimal import Decimal

from apps.data.domain.models import DataType, DataFilter, UnifiedDataItem
from apps.data.repositories.data_repository import DataRepository
from apps.dashboard.persistence.models import Performance, Paper, Student, Budget


@pytest.mark.django_db
class TestDataRepository:
    """DataRepository 테스트"""

    @pytest.fixture
    def data_repository(self):
        """DataRepository 인스턴스"""
        return DataRepository()

    @pytest.fixture
    def sample_performances(self, db):
        """테스트용 Performance 데이터"""
        from apps.accounts.persistence.models import UserProfile
        from uuid import uuid4

        user_id = uuid4()
        user = UserProfile.objects.create(
            id=user_id,
            email="test@example.com",
            full_name="테스트 사용자",
            role="admin"
        )

        performances = [
            Performance.objects.create(
                date=date(2024, 1, 15),
                title="연구과제 A",
                amount=Decimal("1000000"),
                category="연구비",
                uploaded_by=user
            ),
            Performance.objects.create(
                date=date(2024, 2, 20),
                title="특허 출원",
                amount=Decimal("500000"),
                category="특허료",
                uploaded_by=user
            ),
            Performance.objects.create(
                date=date(2023, 12, 10),
                title="기술이전",
                amount=Decimal("3000000"),
                category="기술료",
                uploaded_by=user
            ),
        ]
        return performances

    @pytest.fixture
    def sample_papers(self, db):
        """테스트용 Paper 데이터"""
        from apps.accounts.persistence.models import UserProfile
        from uuid import uuid4

        user_id = uuid4()
        user = UserProfile.objects.create(
            id=user_id,
            email="paper@example.com",
            full_name="논문 작성자",
            role="user"
        )

        papers = [
            Paper.objects.create(
                title="딥러닝 연구",
                authors="홍길동, 김철수",
                publication_date=date(2024, 1, 20),
                field="국제학술지",
                uploaded_by=user
            ),
            Paper.objects.create(
                title="빅데이터 분석",
                authors="이영희",
                publication_date=date(2024, 2, 15),
                field="국내학술지",
                uploaded_by=user
            ),
        ]
        return papers

    # Test Case 1: 데이터 유형 필터링
    def test_get_all_with_type_filter_returns_filtered_data(
        self, data_repository, sample_performances, sample_papers
    ):
        """
        Given: Performance와 Paper 데이터가 존재
        When: type 필터를 'performance'로 설정하여 조회
        Then: Performance 데이터만 반환
        """
        # Arrange
        filters = DataFilter(data_type=DataType.PERFORMANCE)

        # Act
        result = data_repository.get_all_with_filters(filters, page=1, page_size=20)

        # Assert
        assert result.count == 3
        assert all(item.data_type == DataType.PERFORMANCE for item in result.results)

    # Test Case 2: 연도 필터링
    def test_get_all_with_year_filter_returns_filtered_data(
        self, data_repository, sample_performances
    ):
        """
        Given: 2023년과 2024년 데이터가 존재
        When: year 필터를 2024로 설정하여 조회
        Then: 2024년 데이터만 반환
        """
        # Arrange
        filters = DataFilter(year=2024)

        # Act
        result = data_repository.get_all_with_filters(filters, page=1, page_size=20)

        # Assert
        assert result.count == 2  # 2024년 데이터 2개

    # Test Case 3: 검색어 필터링
    def test_search_by_keyword_finds_matching_records(
        self, data_repository, sample_performances
    ):
        """
        Given: Performance 데이터가 존재
        When: '연구과제' 검색어로 조회
        Then: 검색어를 포함한 데이터만 반환
        """
        # Arrange
        filters = DataFilter(search="연구과제")

        # Act
        result = data_repository.get_all_with_filters(filters, page=1, page_size=20)

        # Assert
        assert result.count == 1
        assert result.results[0].title == "연구과제 A"

    # Test Case 4: 정렬 (날짜 내림차순)
    def test_get_all_with_ordering_date_desc_returns_sorted_data(
        self, data_repository, sample_performances
    ):
        """
        Given: 다양한 날짜의 데이터가 존재
        When: 날짜 내림차순으로 정렬
        Then: 최신 데이터가 먼저 반환
        """
        # Arrange
        filters = DataFilter(ordering="-date")

        # Act
        result = data_repository.get_all_with_filters(filters, page=1, page_size=20)

        # Assert
        assert result.results[0].date == date(2024, 2, 20)  # 가장 최신
        assert result.results[-1].date == date(2023, 12, 10)  # 가장 오래된

    # Test Case 5: 정렬 (날짜 오름차순)
    def test_get_all_with_ordering_date_asc_returns_sorted_data(
        self, data_repository, sample_performances
    ):
        """
        Given: 다양한 날짜의 데이터가 존재
        When: 날짜 오름차순으로 정렬
        Then: 오래된 데이터가 먼저 반환
        """
        # Arrange
        filters = DataFilter(ordering="date")

        # Act
        result = data_repository.get_all_with_filters(filters, page=1, page_size=20)

        # Assert
        assert result.results[0].date == date(2023, 12, 10)  # 가장 오래된
        assert result.results[-1].date == date(2024, 2, 20)  # 가장 최신

    # Test Case 6: 페이지네이션
    def test_get_all_applies_pagination(
        self, data_repository, sample_performances
    ):
        """
        Given: 3개의 데이터가 존재
        When: page_size=2로 페이지네이션 적용
        Then: 2개의 결과만 반환
        """
        # Arrange
        filters = DataFilter()

        # Act
        result = data_repository.get_all_with_filters(filters, page=1, page_size=2)

        # Assert
        assert len(result.results) == 2
        assert result.count == 3  # 전체 개수는 3개

    # Test Case 7: 다중 필터 (AND 조건)
    def test_get_all_with_multiple_filters_returns_filtered_data(
        self, data_repository, sample_performances
    ):
        """
        Given: Performance 데이터가 존재
        When: type='performance', year=2024, search='연구' 필터 적용
        Then: 모든 조건을 만족하는 데이터만 반환
        """
        # Arrange
        filters = DataFilter(
            data_type=DataType.PERFORMANCE,
            year=2024,
            search="연구"
        )

        # Act
        result = data_repository.get_all_with_filters(filters, page=1, page_size=20)

        # Assert
        assert result.count == 1
        assert result.results[0].title == "연구과제 A"

    # Test Case 8: 빈 결과
    def test_get_all_returns_empty_when_no_match(
        self, data_repository, sample_performances
    ):
        """
        Given: Performance 데이터가 존재
        When: 존재하지 않는 검색어로 조회
        Then: 빈 결과 반환
        """
        # Arrange
        filters = DataFilter(search="존재하지않는검색어")

        # Act
        result = data_repository.get_all_with_filters(filters, page=1, page_size=20)

        # Assert
        assert result.count == 0
        assert len(result.results) == 0

    # Test Case 9: ID로 단일 조회
    def test_get_by_id_returns_data_item(
        self, data_repository, sample_performances
    ):
        """
        Given: Performance 데이터가 존재
        When: 특정 ID로 조회
        Then: 해당 데이터 반환
        """
        # Arrange
        performance = sample_performances[0]

        # Act
        result = data_repository.get_by_id(DataType.PERFORMANCE, performance.id)

        # Assert
        assert result is not None
        assert result.id == performance.id
        assert result.title == "연구과제 A"

    # Test Case 10: 존재하지 않는 ID 조회
    def test_get_by_id_returns_none_when_not_found(
        self, data_repository
    ):
        """
        Given: 데이터가 없음
        When: 존재하지 않는 ID로 조회
        Then: None 반환
        """
        # Arrange & Act
        result = data_repository.get_by_id(DataType.PERFORMANCE, 99999)

        # Assert
        assert result is None
