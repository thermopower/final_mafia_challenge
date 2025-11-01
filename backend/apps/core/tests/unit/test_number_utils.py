"""
NumberUtils 단위 테스트
"""
from decimal import Decimal
import pytest


class TestNumberUtils:
    """NumberUtils 단위 테스트"""

    def test_parse_decimal_with_commas(self):
        # Arrange
        from apps.core.utils.number_utils import NumberUtils
        value = "1,200,000"

        # Act
        result = NumberUtils.parse_decimal(value)

        # Assert
        assert result == Decimal("1200000")

    def test_parse_decimal_with_percent(self):
        # Arrange
        from apps.core.utils.number_utils import NumberUtils
        value = "85.5%"

        # Act
        result = NumberUtils.parse_decimal(value)

        # Assert
        assert result == Decimal("85.5")

    def test_parse_decimal_plain_number(self):
        # Arrange
        from apps.core.utils.number_utils import NumberUtils
        value = "1200000"

        # Act
        result = NumberUtils.parse_decimal(value)

        # Assert
        assert result == Decimal("1200000")

    def test_parse_decimal_invalid_string_returns_none(self):
        # Arrange
        from apps.core.utils.number_utils import NumberUtils
        value = "백만원"

        # Act
        result = NumberUtils.parse_decimal(value)

        # Assert
        assert result is None

    def test_format_currency_adds_commas(self):
        # Arrange
        from apps.core.utils.number_utils import NumberUtils
        amount = Decimal("1200000")

        # Act
        result = NumberUtils.format_currency(amount)

        # Assert
        assert result == "1,200,000"

    def test_format_currency_with_decimal_places(self):
        # Arrange
        from apps.core.utils.number_utils import NumberUtils
        amount = Decimal("1200000.50")

        # Act
        result = NumberUtils.format_currency(amount)

        # Assert
        assert result == "1,200,000.50"
