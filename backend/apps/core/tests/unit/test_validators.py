"""
CommonValidator 단위 테스트

TDD Red Phase: 테스트 먼저 작성
"""
import pytest
from decimal import Decimal


class TestCommonValidator:
    """CommonValidator 단위 테스트"""

    # 이메일 검증
    def test_validate_email_returns_true_for_valid_email(self):
        # Arrange
        from apps.core.validators import CommonValidator
        email = "test@example.com"

        # Act
        result = CommonValidator.validate_email(email)

        # Assert
        assert result is True

    def test_validate_email_returns_false_for_invalid_email(self):
        # Arrange
        from apps.core.validators import CommonValidator
        email = "invalid-email"

        # Act
        result = CommonValidator.validate_email(email)

        # Assert
        assert result is False

    # 날짜 검증
    def test_validate_date_returns_true_for_valid_date(self):
        # Arrange
        from apps.core.validators import CommonValidator
        date_str = "2024-11-01"

        # Act
        result = CommonValidator.validate_date(date_str)

        # Assert
        assert result is True

    def test_validate_date_returns_false_for_invalid_date(self):
        # Arrange
        from apps.core.validators import CommonValidator
        date_str = "2024/13/01"

        # Act
        result = CommonValidator.validate_date(date_str)

        # Assert
        assert result is False

    # 양수 검증
    def test_validate_positive_number_returns_true_for_positive(self):
        # Arrange
        from apps.core.validators import CommonValidator
        value = Decimal("100")

        # Act
        result = CommonValidator.validate_positive_number(value)

        # Assert
        assert result is True

    def test_validate_positive_number_returns_false_for_negative(self):
        # Arrange
        from apps.core.validators import CommonValidator
        value = Decimal("-100")

        # Act
        result = CommonValidator.validate_positive_number(value)

        # Assert
        assert result is False

    def test_validate_positive_number_returns_false_for_zero(self):
        # Arrange
        from apps.core.validators import CommonValidator
        value = Decimal("0")

        # Act
        result = CommonValidator.validate_positive_number(value)

        # Assert
        assert result is False

    # 필수 필드 검증
    def test_validate_required_fields_returns_true_when_all_present(self):
        # Arrange
        from apps.core.validators import CommonValidator
        data = {"name": "홍길동", "email": "test@example.com"}
        required_fields = ["name", "email"]

        # Act
        is_valid, missing = CommonValidator.validate_required_fields(data, required_fields)

        # Assert
        assert is_valid is True
        assert missing == []

    def test_validate_required_fields_returns_false_when_missing(self):
        # Arrange
        from apps.core.validators import CommonValidator
        data = {"name": "홍길동"}
        required_fields = ["name", "email", "phone"]

        # Act
        is_valid, missing = CommonValidator.validate_required_fields(data, required_fields)

        # Assert
        assert is_valid is False
        assert set(missing) == {"email", "phone"}
