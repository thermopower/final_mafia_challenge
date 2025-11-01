"""
글로벌 예외 핸들러 단위 테스트

TDD Red Phase: 테스트 먼저 작성
"""
import pytest
from unittest.mock import Mock
from apps.core.exceptions import (
    ValidationError,
    AuthenticationError,
    PermissionDeniedError,
    ResourceNotFoundError,
)


class TestExceptionHandler:
    """글로벌 예외 핸들러 테스트"""

    def test_handles_validation_error(self):
        """ValidationError를 JSON 응답으로 변환하는지 테스트"""
        # Arrange
        from infrastructure.middleware.exception_handler import exception_handler

        exc = ValidationError(message="금액이 음수입니다")
        context = {}

        # Act
        response = exception_handler(exc, context)

        # Assert
        assert response.status_code == 400
        assert response.data["error"] == "금액이 음수입니다"
        assert "code" in response.data

    def test_handles_authentication_error(self):
        """AuthenticationError를 JSON 응답으로 변환하는지 테스트"""
        # Arrange
        from infrastructure.middleware.exception_handler import exception_handler

        exc = AuthenticationError()
        context = {}

        # Act
        response = exception_handler(exc, context)

        # Assert
        assert response.status_code == 401
        assert response.data["error"] == "인증이 필요합니다"

    def test_handles_permission_denied_error(self):
        """PermissionDeniedError를 JSON 응답으로 변환하는지 테스트"""
        # Arrange
        from infrastructure.middleware.exception_handler import exception_handler

        exc = PermissionDeniedError()
        context = {}

        # Act
        response = exception_handler(exc, context)

        # Assert
        assert response.status_code == 403
        assert response.data["error"] == "접근 권한이 없습니다"

    def test_handles_resource_not_found_error(self):
        """ResourceNotFoundError를 JSON 응답으로 변환하는지 테스트"""
        # Arrange
        from infrastructure.middleware.exception_handler import exception_handler

        exc = ResourceNotFoundError()
        context = {}

        # Act
        response = exception_handler(exc, context)

        # Assert
        assert response.status_code == 404
        assert response.data["error"] == "요청한 리소스를 찾을 수 없습니다"

    def test_handles_unexpected_exception_returns_500(self):
        """예상치 못한 예외는 500으로 반환하는지 테스트"""
        # Arrange
        from infrastructure.middleware.exception_handler import exception_handler

        exc = Exception("예상치 못한 오류")
        context = {}

        # Act
        response = exception_handler(exc, context)

        # Assert
        assert response.status_code == 500
        assert "서버 오류" in response.data["error"]

    def test_response_has_consistent_format(self):
        """응답 형식이 일관되는지 테스트"""
        # Arrange
        from infrastructure.middleware.exception_handler import exception_handler

        exc = ValidationError(message="테스트 오류")
        context = {}

        # Act
        response = exception_handler(exc, context)

        # Assert
        assert "error" in response.data
        assert "code" in response.data
        assert isinstance(response.data, dict)
