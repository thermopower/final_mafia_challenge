# -*- coding: utf-8 -*-
"""
ResearchProject CSV Parser

연구 과제 데이터 CSV 파일 파싱
"""
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd


class ResearchProjectParser:
    """
    연구 과제 CSV 파서

    CSV 구조:
        집행ID, 과제번호, 과제명, 연구책임자, 소속학과, 지원기관,
        총연구비, 집행일자, 집행항목, 집행금액, 상태, 비고
    """

    REQUIRED_COLUMNS = [
        '집행ID',
        '과제번호',
        '과제명',
        '연구책임자',
        '소속학과',
        '지원기관',
        '총연구비',
        '집행일자',
        '집행항목',
        '집행금액',
        '상태',
        '비고'
    ]

    @classmethod
    def parse(cls, file_path: str) -> List[Dict]:
        """
        CSV 파일 파싱

        Args:
            file_path: CSV 파일 경로

        Returns:
            List[Dict]: 파싱된 데이터 리스트

        Raises:
            ValueError: 필수 컬럼 누락 시
        """
        # CSV 파일 읽기 (UTF-8 인코딩)
        df = pd.read_csv(file_path, encoding='utf-8-sig')

        # 컬럼명 정규화
        df.columns = df.columns.str.strip()

        # 필수 컬럼 검증
        missing_columns = set(cls.REQUIRED_COLUMNS) - set(df.columns)
        if missing_columns:
            raise ValueError(f"필수 컬럼이 누락되었습니다: {', '.join(missing_columns)}")

        # 데이터 파싱
        parsed_data = []
        for idx, row in df.iterrows():
            try:
                # 집행일자 파싱 (YYYY-MM-DD 형식)
                execution_date = pd.to_datetime(row['집행일자']).date()

                # 비고 처리 (빈 값 허용)
                remarks = str(row['비고']).strip() if pd.notna(row['비고']) else None

                data = {
                    'execution_id': str(row['집행ID']).strip(),
                    'project_number': str(row['과제번호']).strip(),
                    'project_name': str(row['과제명']).strip(),
                    'principal_investigator': str(row['연구책임자']).strip(),
                    'department': str(row['소속학과']).strip(),
                    'funding_agency': str(row['지원기관']).strip(),
                    'total_budget': int(row['총연구비']),
                    'execution_date': execution_date,
                    'execution_item': str(row['집행항목']).strip(),
                    'execution_amount': int(row['집행금액']),
                    'status': str(row['상태']).strip(),
                    'remarks': remarks
                }
                parsed_data.append(data)
            except (ValueError, KeyError, TypeError) as e:
                raise ValueError(f"{idx + 2}행 파싱 오류: {str(e)}")

        return parsed_data
