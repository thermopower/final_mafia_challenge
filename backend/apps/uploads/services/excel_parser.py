"""
Excel 파서

openpyxl을 사용하여 Excel 파일을 파싱합니다.
"""
import openpyxl
from typing import List, Dict
from apps.uploads.domain.models import ParsedData
from apps.core.exceptions import ValidationError


class ExcelParser:
    """Excel 파일 파서"""

    def parse(self, file_path: str) -> ParsedData:
        """
        Excel 파일 파싱

        Args:
            file_path: Excel 파일 경로

        Returns:
            ParsedData: 헤더, 데이터 행, 총 행 수

        Raises:
            ValidationError: 파일 파싱 실패 시
        """
        try:
            workbook = openpyxl.load_workbook(file_path)
            worksheet = workbook.active

            headers = self._extract_headers(worksheet)
            rows = self._extract_rows(worksheet, start_row=2)

            if not rows:
                raise ValidationError("파일이 비어있습니다")

            return ParsedData(headers=headers, rows=rows, total_rows=len(rows))

        except openpyxl.utils.exceptions.InvalidFileException:
            raise ValidationError("파일이 손상되었거나 올바른 Excel 형식이 아닙니다")
        except Exception as e:
            raise ValidationError(f"파일 파싱 중 오류 발생: {str(e)}")

    def _extract_headers(self, worksheet) -> List[str]:
        """헤더 행 추출 (1행)"""
        headers = []
        for cell in worksheet[1]:
            if cell.value:
                headers.append(str(cell.value).strip())
        return headers

    def _extract_rows(self, worksheet, start_row: int) -> List[Dict]:
        """데이터 행 추출 (2행부터)"""
        headers = self._extract_headers(worksheet)
        rows = []

        for row_idx, row in enumerate(
            worksheet.iter_rows(min_row=start_row), start=start_row
        ):
            row_data = {}
            for col_idx, cell in enumerate(row):
                if col_idx < len(headers):
                    row_data[headers[col_idx]] = cell.value

            # 빈 행 제외
            if any(row_data.values()):
                rows.append(row_data)

        return rows
