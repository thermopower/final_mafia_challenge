"""
DateUtils 단위 테스트
"""
import datetime
import pytest


class TestDateUtils:
    """DateUtils 단위 테스트"""

    def test_parse_date_with_dash_format(self):
        # Arrange
        from apps.core.utils.date_utils import DateUtils
        date_str = "2024-11-01"

        # Act
        result = DateUtils.parse_date(date_str)

        # Assert
        assert result == datetime.date(2024, 11, 1)

    def test_parse_date_with_slash_format(self):
        # Arrange
        from apps.core.utils.date_utils import DateUtils
        date_str = "2024/11/01"

        # Act
        result = DateUtils.parse_date(date_str)

        # Assert
        assert result == datetime.date(2024, 11, 1)

    def test_parse_date_with_dot_format(self):
        # Arrange
        from apps.core.utils.date_utils import DateUtils
        date_str = "2024.11.01"

        # Act
        result = DateUtils.parse_date(date_str)

        # Assert
        assert result == datetime.date(2024, 11, 1)

    def test_parse_date_with_invalid_format_returns_none(self):
        # Arrange
        from apps.core.utils.date_utils import DateUtils
        date_str = "작년"

        # Act
        result = DateUtils.parse_date(date_str)

        # Assert
        assert result is None

    def test_format_date_returns_yyyy_mm_dd(self):
        # Arrange
        from apps.core.utils.date_utils import DateUtils
        date_obj = datetime.date(2024, 11, 1)

        # Act
        result = DateUtils.format_date(date_obj)

        # Assert
        assert result == "2024-11-01"
