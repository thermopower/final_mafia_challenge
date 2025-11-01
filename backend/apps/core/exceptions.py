"""
커스텀 예외 클래스

비즈니스 로직 예외를 정의하고 HTTP 상태 코드와 오류 메시지를 매핑합니다.
"""


class BaseAPIException(Exception):
    """기본 API 예외 클래스"""
    status_code = 500
    default_message = "서버 오류가 발생했습니다"

    def __init__(self, message: str = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class ValidationError(BaseAPIException):
    """데이터 검증 오류 (400)"""
    status_code = 400
    default_message = "입력 데이터가 유효하지 않습니다"


class AuthenticationError(BaseAPIException):
    """인증 오류 (401)"""
    status_code = 401
    default_message = "인증이 필요합니다"


class PermissionDeniedError(BaseAPIException):
    """권한 오류 (403)"""
    status_code = 403
    default_message = "접근 권한이 없습니다"


class ResourceNotFoundError(BaseAPIException):
    """리소스 없음 (404)"""
    status_code = 404
    default_message = "요청한 리소스를 찾을 수 없습니다"


class FileProcessingError(BaseAPIException):
    """파일 처리 오류 (400)"""
    status_code = 400
    default_message = "파일 처리 중 오류가 발생했습니다"
