"""
컬럼 매퍼

데이터 유형별 필수 컬럼 및 타입 정의
"""
from datetime import date
from decimal import Decimal


class ColumnMapper:
    """데이터 유형별 컬럼 정의"""

    PERFORMANCE_COLUMNS = {
        "required": ["날짜", "금액", "카테고리"],
        "optional": ["항목", "비고"],
    }

    PAPER_COLUMNS = {
        "required": ["제목", "저자", "게재일", "분야"],
        "optional": ["저널명", "DOI"],
    }

    STUDENT_COLUMNS = {
        "required": ["학번", "이름", "학과", "학년"],
        "optional": ["연락처", "이메일"],
    }

    BUDGET_COLUMNS = {
        "required": ["항목", "금액", "카테고리"],
        "optional": ["비고"],
    }

    COLUMN_TYPES = {
        "performance": {
            "날짜": date,
            "금액": Decimal,
            "카테고리": str,
            "항목": str,
            "비고": str,
        },
        "paper": {
            "제목": str,
            "저자": str,
            "게재일": date,
            "분야": str,
            "저널명": str,
            "DOI": str,
        },
        "student": {
            "학번": str,
            "이름": str,
            "학과": str,
            "학년": int,
            "연락처": str,
            "이메일": str,
        },
        "budget": {
            "항목": str,
            "금액": Decimal,
            "카테고리": str,
            "비고": str,
        },
    }

    @staticmethod
    def get_required_columns(data_type: str) -> list[str]:
        """
        데이터 유형별 필수 컬럼 반환

        Args:
            data_type: 데이터 유형 ('performance', 'paper', 'student', 'budget')

        Returns:
            필수 컬럼 목록
        """
        column_map = {
            "performance": ColumnMapper.PERFORMANCE_COLUMNS,
            "paper": ColumnMapper.PAPER_COLUMNS,
            "student": ColumnMapper.STUDENT_COLUMNS,
            "budget": ColumnMapper.BUDGET_COLUMNS,
        }

        if data_type not in column_map:
            raise ValueError(f"Invalid data_type: {data_type}")

        return column_map[data_type]["required"]

    @staticmethod
    def get_column_types(data_type: str) -> dict:
        """
        데이터 유형별 컬럼 타입 반환

        Args:
            data_type: 데이터 유형

        Returns:
            {컬럼명: 타입} 딕셔너리
        """
        if data_type not in ColumnMapper.COLUMN_TYPES:
            raise ValueError(f"Invalid data_type: {data_type}")

        return ColumnMapper.COLUMN_TYPES[data_type]
