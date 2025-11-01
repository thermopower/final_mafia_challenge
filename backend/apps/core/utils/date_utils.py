"""
날짜 변환 유틸리티

다양한 날짜 형식 파싱 및 변환을 제공합니다.
"""
import datetime
from typing import Optional


class DateUtils:
    """날짜 유틸리티 클래스"""

    DATE_FORMATS = [
        "%Y-%m-%d",  # 2024-11-01
        "%Y/%m/%d",  # 2024/11/01
        "%Y.%m.%d",  # 2024.11.01
    ]

    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime.date]:
        """
        다양한 형식의 날짜 문자열을 date 객체로 변환

        지원 형식:
        - YYYY-MM-DD
        - YYYY/MM/DD
        - YYYY.MM.DD

        Args:
            date_str: 날짜 문자열

        Returns:
            datetime.date 또는 None (파싱 실패 시)
        """
        if not date_str or not isinstance(date_str, str):
            return None

        for date_format in DateUtils.DATE_FORMATS:
            try:
                return datetime.datetime.strptime(date_str, date_format).date()
            except ValueError:
                continue

        return None

    @staticmethod
    def format_date(date_obj: datetime.date) -> str:
        """
        date 객체를 YYYY-MM-DD 형식으로 변환

        Args:
            date_obj: datetime.date 객체

        Returns:
            YYYY-MM-DD 형식의 문자열
        """
        if not isinstance(date_obj, datetime.date):
            raise ValueError("date_obj must be a datetime.date instance")

        return date_obj.strftime("%Y-%m-%d")
