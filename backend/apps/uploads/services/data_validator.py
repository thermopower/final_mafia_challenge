"""
데이터 검증기

필수 컬럼, 데이터 타입, 중복 데이터를 검증합니다.
"""
from typing import List, Dict
from apps.uploads.domain.models import ValidationResult
from apps.uploads.services.column_mapper import ColumnMapper
from apps.core.utils.date_utils import DateUtils
from apps.core.utils.number_utils import NumberUtils
from decimal import Decimal
from datetime import date


class DataValidator:
    """데이터 검증기"""

    def validate(self, data: List[Dict], data_type: str) -> ValidationResult:
        """
        데이터 검증

        Args:
            data: 파싱된 데이터
            data_type: 데이터 유형

        Returns:
            ValidationResult: 검증 결과
        """
        required_columns = ColumnMapper.get_required_columns(data_type)
        column_types = ColumnMapper.get_column_types(data_type)

        # 필수 컬럼 검증
        missing_columns = self._validate_required_columns(data, required_columns)
        if missing_columns:
            return ValidationResult(
                is_valid=False,
                missing_columns=missing_columns,
                invalid_rows=[],
                duplicates=[],
            )

        # 데이터 타입 검증
        invalid_rows = self._validate_data_types(data, column_types)
        if invalid_rows:
            return ValidationResult(
                is_valid=False,
                missing_columns=[],
                invalid_rows=invalid_rows,
                duplicates=[],
            )

        # 중복 데이터 검사 (간략화: 날짜+카테고리 또는 학번)
        duplicates = self._check_duplicates(data, data_type)
        if duplicates:
            return ValidationResult(
                is_valid=False,
                missing_columns=[],
                invalid_rows=[],
                duplicates=duplicates,
            )

        return ValidationResult(
            is_valid=True, missing_columns=[], invalid_rows=[], duplicates=[]
        )

    def _validate_required_columns(
        self, data: List[Dict], required_columns: List[str]
    ) -> List[str]:
        """필수 컬럼 검증"""
        if not data:
            return required_columns

        headers = set(data[0].keys())
        missing = [col for col in required_columns if col not in headers]
        return missing

    def _validate_data_types(
        self, data: List[Dict], column_types: Dict
    ) -> List[Dict]:
        """데이터 타입 검증"""
        invalid_rows = []

        for row_idx, row in enumerate(data, start=2):  # Excel 2행부터 시작
            for column, expected_type in column_types.items():
                if column not in row:
                    continue

                value = row[column]
                if value is None:
                    continue

                try:
                    if expected_type == date:
                        parsed = DateUtils.parse_date(str(value))
                        if not parsed:
                            invalid_rows.append(
                                {
                                    "row": row_idx,
                                    "column": column,
                                    "value": str(value),
                                    "message": "날짜 형식이 아닙니다 (YYYY-MM-DD 필요)",
                                }
                            )
                    elif expected_type == Decimal:
                        parsed = NumberUtils.parse_decimal(str(value))
                        if parsed is None:
                            invalid_rows.append(
                                {
                                    "row": row_idx,
                                    "column": column,
                                    "value": str(value),
                                    "message": "숫자가 아닙니다",
                                }
                            )
                    elif expected_type == int:
                        try:
                            int(value)
                        except (ValueError, TypeError):
                            invalid_rows.append(
                                {
                                    "row": row_idx,
                                    "column": column,
                                    "value": str(value),
                                    "message": "정수가 아닙니다",
                                }
                            )
                except Exception as e:
                    invalid_rows.append(
                        {
                            "row": row_idx,
                            "column": column,
                            "value": str(value),
                            "message": str(e),
                        }
                    )

        return invalid_rows

    def _check_duplicates(self, data: List[Dict], data_type: str) -> List[Dict]:
        """중복 데이터 검사 (간략화)"""
        # 실제 구현 시 데이터베이스와 비교 필요
        # 여기서는 파일 내 중복만 체크
        seen = set()
        duplicates = []

        for row_idx, row in enumerate(data, start=2):
            if data_type in ["performance", "budget"]:
                key = f"{row.get('날짜')}-{row.get('카테고리')}"
            elif data_type == "student":
                key = row.get("학번")
            elif data_type == "paper":
                key = row.get("제목")
            else:
                continue

            if key in seen:
                duplicates.append(
                    {
                        "row": row_idx,
                        "key": key,
                        "message": f"{key}는 이미 존재합니다",
                    }
                )
            seen.add(key)

        return duplicates
