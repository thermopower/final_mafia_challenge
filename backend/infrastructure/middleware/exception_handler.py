"""
DRF 글로벌 예외 핸들러

모든 예외를 일관된 JSON 형식으로 변환합니다.
"""
import logging
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from apps.core.exceptions import BaseAPIException

logger = logging.getLogger(__name__)


def exception_handler(exc, context):
    """
    DRF 글로벌 예외 핸들러

    Response 형식:
    {
        "error": "오류 메시지",
        "code": "ERROR_CODE",
        "details": {...}  # 개발 환경만
    }
    """
    # DRF 기본 예외 핸들러 먼저 호출
    response = drf_exception_handler(exc, context)

    # 커스텀 예외 처리
    if isinstance(exc, BaseAPIException):
        response_data = {
            "error": exc.message,
            "code": exc.__class__.__name__.upper(),
        }

        # 로깅
        logger.warning(
            f"API Exception: {exc.__class__.__name__} - {exc.message}",
            extra={
                "exception_type": exc.__class__.__name__,
                "status_code": exc.status_code,
            },
        )

        return Response(response_data, status=exc.status_code)

    # DRF가 처리한 예외 (response가 이미 생성됨)
    if response is not None:
        return response

    # 예상치 못한 예외 (500 Internal Server Error)
    logger.error(
        f"Unexpected exception: {exc}",
        exc_info=True,
        extra={"exception_type": type(exc).__name__},
    )

    return Response(
        {
            "error": "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "code": "INTERNAL_SERVER_ERROR",
        },
        status=500,
    )
