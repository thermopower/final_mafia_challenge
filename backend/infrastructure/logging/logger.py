"""
구조화된 로거

일관된 로그 형식으로 API 요청, 오류, 파일 업로드 등을 기록합니다.
"""
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def get_logger(name: str = None) -> logging.Logger:
    """
    로거 인스턴스 반환

    Args:
        name: 로거 이름 (기본값: 호출 모듈 이름)

    Returns:
        logging.Logger
    """
    return logging.getLogger(name if name else __name__)


class StructuredLogger:
    """구조화된 로깅을 제공하는 클래스"""

    @staticmethod
    def log_api_request(method: str, path: str, user_id: str = None):
        """
        API 요청 로깅

        Args:
            method: HTTP 메서드 (GET, POST 등)
            path: 요청 경로
            user_id: 사용자 ID (선택)
        """
        logger.info(
            f"API Request: {method} {path}",
            extra={"method": method, "path": path, "user_id": user_id},
        )

    @staticmethod
    def log_error(error: Exception, context: Dict = None):
        """
        오류 로깅

        Args:
            error: 발생한 예외
            context: 추가 컨텍스트 정보
        """
        logger.error(
            f"Error: {str(error)}",
            exc_info=True,
            extra={"error_type": type(error).__name__, "context": context or {}},
        )

    @staticmethod
    def log_file_upload(filename: str, data_type: str, rows: int, user_id: str):
        """
        파일 업로드 로깅

        Args:
            filename: 파일명
            data_type: 데이터 유형
            rows: 처리된 행 수
            user_id: 업로드한 사용자 ID
        """
        logger.info(
            f"File Upload: {filename} ({data_type}, {rows} rows)",
            extra={
                "filename": filename,
                "data_type": data_type,
                "rows": rows,
                "user_id": user_id,
            },
        )
