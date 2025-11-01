"""
커스텀 예외 클래스 단위 테스트

TDD Red Phase: 테스트 먼저 작성
"""
import pytest


class TestBaseAPIException:
    """BaseAPIException 단위 테스트"""

    def test_base_api_exception_has_default_message(self):
        """기본 메시지를 가지는지 테스트"""
        # Arrange & Act
        from apps.core.exceptions import BaseAPIException
        exception = BaseAPIException()

        # Assert
        assert exception.message == "서버 오류가 발생했습니다"
        assert exception.status_code == 500

    def test_base_api_exception_accepts_custom_message(self):
        """커스텀 메시지를 받을 수 있는지 테스트"""
        # Arrange
        from apps.core.exceptions import BaseAPIException
        custom_message = "커스텀 오류 메시지"

        # Act
        exception = BaseAPIException(message=custom_message)

        # Assert
        assert exception.message == custom_message


class TestValidationError:
    """ValidationError 단위 테스트"""

    def test_validation_error_has_400_status_code(self):
        """ValidationError가 400 상태 코드를 가지는지 테스트"""
        # Arrange & Act
        from apps.core.exceptions import ValidationError
        exception = ValidationError()

        # Assert
        assert exception.status_code == 400
        assert exception.message == "입력 데이터가 유효하지 않습니다"

    def test_validation_error_accepts_custom_message(self):
        """ValidationError가 커스텀 메시지를 받을 수 있는지 테스트"""
        # Arrange
        from apps.core.exceptions import ValidationError
        custom_message = "금액이 음수입니다"

        # Act
        exception = ValidationError(message=custom_message)

        # Assert
        assert exception.message == custom_message
        assert exception.status_code == 400


class TestAuthenticationError:
    """AuthenticationError 단위 테스트"""

    def test_authentication_error_has_401_status_code(self):
        """AuthenticationError가 401 상태 코드를 가지는지 테스트"""
        # Arrange & Act
        from apps.core.exceptions import AuthenticationError
        exception = AuthenticationError()

        # Assert
        assert exception.status_code == 401
        assert exception.message == "인증이 필요합니다"


class TestPermissionDeniedError:
    """PermissionDeniedError 단위 테스트"""

    def test_permission_denied_error_has_403_status_code(self):
        """PermissionDeniedError가 403 상태 코드를 가지는지 테스트"""
        # Arrange & Act
        from apps.core.exceptions import PermissionDeniedError
        exception = PermissionDeniedError()

        # Assert
        assert exception.status_code == 403
        assert exception.message == "접근 권한이 없습니다"


class TestResourceNotFoundError:
    """ResourceNotFoundError 단위 테스트"""

    def test_resource_not_found_error_has_404_status_code(self):
        """ResourceNotFoundError가 404 상태 코드를 가지는지 테스트"""
        # Arrange & Act
        from apps.core.exceptions import ResourceNotFoundError
        exception = ResourceNotFoundError()

        # Assert
        assert exception.status_code == 404
        assert exception.message == "요청한 리소스를 찾을 수 없습니다"


class TestFileProcessingError:
    """FileProcessingError 단위 테스트"""

    def test_file_processing_error_has_400_status_code(self):
        """FileProcessingError가 400 상태 코드를 가지는지 테스트"""
        # Arrange & Act
        from apps.core.exceptions import FileProcessingError
        exception = FileProcessingError()

        # Assert
        assert exception.status_code == 400
        assert exception.message == "파일 처리 중 오류가 발생했습니다"
