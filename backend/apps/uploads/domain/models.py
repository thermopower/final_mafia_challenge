"""
업로드 도메인 모델

순수 비즈니스 엔티티 정의 (프레임워크 독립적)
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class UploadRecord:
    """업로드 이력 도메인 모델"""

    id: Optional[int]
    filename: str
    data_type: str  # 'performance', 'paper', 'student', 'budget'
    rows_processed: int
    uploaded_at: datetime
    uploaded_by: str  # 사용자 이메일
    status: str  # 'success', 'failed', 'partial'


@dataclass
class ParsedData:
    """파싱된 Excel 데이터"""

    headers: List[str]
    rows: List[Dict]
    total_rows: int


@dataclass
class ValidationResult:
    """데이터 검증 결과"""

    is_valid: bool
    missing_columns: List[str]
    invalid_rows: List[Dict]  # {'row': int, 'column': str, 'value': str, 'message': str}
    duplicates: List[Dict]  # {'row': int, 'key': str, 'message': str}


@dataclass
class UploadResult:
    """업로드 처리 결과"""

    success: bool
    upload_record: UploadRecord
    errors: Optional[List[str]]
