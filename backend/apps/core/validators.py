"""
공통 Validator 클래스

이메일, 날짜, 숫자, 필수 필드 검증을 제공합니다.
"""
import re
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Tuple, Union


class CommonValidator:
    """공통 데이터 검증 클래스"""

    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    DATE_FORMAT = "%Y-%m-%d"

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        이메일 형식 검증

        Args:
            email: 검증할 이메일 주소

        Returns:
            True if valid, False otherwise
        """
        if not email or not isinstance(email, str):
            return False

        return CommonValidator.EMAIL_REGEX.match(email) is not None

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """
        날짜 형식 검증 (YYYY-MM-DD)

        Args:
            date_str: 검증할 날짜 문자열

        Returns:
            True if valid, False otherwise
        """
        if not date_str or not isinstance(date_str, str):
            return False

        try:
            datetime.strptime(date_str, CommonValidator.DATE_FORMAT)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_positive_number(value: Union[int, Decimal]) -> bool:
        """
        양수 검증 (0은 제외)

        Args:
            value: 검증할 숫자

        Returns:
            True if positive (> 0), False otherwise
        """
        if value is None:
            return False

        try:
            return Decimal(str(value)) > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_required_fields(
        data: Dict, required_fields: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        필수 필드 검증

        Args:
            data: 검증할 데이터 딕셔너리
            required_fields: 필수 필드 목록

        Returns:
            (is_valid, missing_fields) 튜플
        """
        if not data or not isinstance(data, dict):
            return False, required_fields

        missing_fields = [field for field in required_fields if field not in data]

        return len(missing_fields) == 0, missing_fields
