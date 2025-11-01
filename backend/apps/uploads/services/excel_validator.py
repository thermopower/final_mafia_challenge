"""
엑셀 파일 검증기

파일 형식, 크기, 필수 컬럼을 검증합니다.
"""
from typing import List, Tuple


class ExcelFileValidator:
    """엑셀 파일 검증 클래스"""

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = [".xlsx", ".xls"]

    REQUIRED_COLUMNS = {
        "performance": ["날짜", "금액", "카테고리"],
        "paper": ["제목", "저자", "게재일", "분야"],
        "student": ["학번", "이름", "학과", "학년"],
        "budget": ["항목", "금액", "카테고리"],
    }

    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """
        파일 확장자 검증

        Args:
            filename: 파일명

        Returns:
            True if valid, False otherwise
        """
        if not filename:
            return False

        return any(
            filename.lower().endswith(ext)
            for ext in ExcelFileValidator.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """
        파일 크기 검증

        Args:
            file_size: 파일 크기 (bytes)

        Returns:
            True if valid (≤ 10MB), False otherwise
        """
        return 0 < file_size <= ExcelFileValidator.MAX_FILE_SIZE

    @staticmethod
    def validate_required_columns(
        headers: List[str], data_type: str
    ) -> Tuple[bool, List[str]]:
        """
        필수 컬럼 검증

        Args:
            headers: 엑셀 헤더 목록
            data_type: 데이터 유형 (performance, paper, student, budget)

        Returns:
            (is_valid, missing_columns) 튜플
        """
        if data_type not in ExcelFileValidator.REQUIRED_COLUMNS:
            return False, ["Invalid data_type"]

        required = ExcelFileValidator.REQUIRED_COLUMNS[data_type]
        missing = [col for col in required if col not in headers]

        return len(missing) == 0, missing
