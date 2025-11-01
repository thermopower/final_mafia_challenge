"""
숫자 변환 유틸리티

쉼표, 퍼센트 포함 문자열을 Decimal로 변환합니다.
"""
from decimal import Decimal, InvalidOperation
from typing import Optional


class NumberUtils:
    """숫자 유틸리티 클래스"""

    @staticmethod
    def parse_decimal(value: str) -> Optional[Decimal]:
        """
        문자열을 Decimal로 변환

        지원 형식:
        - "1,200,000" → Decimal("1200000")
        - "85.5%" → Decimal("85.5")
        - "1200000" → Decimal("1200000")

        Args:
            value: 변환할 문자열

        Returns:
            Decimal 또는 None (변환 실패 시)
        """
        if not value or not isinstance(value, str):
            return None

        try:
            # 쉼표 제거
            value = value.replace(",", "")

            # 퍼센트 기호 제거
            if value.endswith("%"):
                value = value[:-1]

            return Decimal(value)
        except (ValueError, InvalidOperation):
            return None

    @staticmethod
    def format_currency(amount: Decimal) -> str:
        """
        금액을 천 단위 쉼표 형식으로 변환

        Args:
            amount: Decimal 금액

        Returns:
            천 단위 쉼표 포함 문자열 (예: "1,200,000")
        """
        if not isinstance(amount, (Decimal, int, float)):
            raise ValueError("amount must be a number")

        # 정수 부분과 소수 부분 분리
        amount_str = str(amount)

        if "." in amount_str:
            integer_part, decimal_part = amount_str.split(".")
        else:
            integer_part = amount_str
            decimal_part = None

        # 천 단위 쉼표 추가
        integer_part = "{:,}".format(int(integer_part))

        if decimal_part:
            return f"{integer_part}.{decimal_part}"
        else:
            return integer_part
