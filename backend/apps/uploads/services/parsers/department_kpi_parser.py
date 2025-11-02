# -*- coding: utf-8 -*-
"""
DepartmentKPI CSV Parser

학과 KPI 데이터 CSV 파일 파싱
"""
from typing import List, Dict
from decimal import Decimal
import pandas as pd


class DepartmentKPIParser:
    """
    학과 KPI CSV 파서

    CSV 구조:
        평가년도, 단과대학, 학과, 졸업생 취업률 (%), 전임교원 수 (명),
        초빙교원 수 (명), 연간 기술이전 수입액 (억원), 국제학술대회 개최 횟수
    """

    REQUIRED_COLUMNS = [
        '평가년도',
        '단과대학',
        '학과',
        '졸업생 취업률 (%)',
        '전임교원 수 (명)',
        '초빙교원 수 (명)',
        '연간 기술이전 수입액 (억원)',
        '국제학술대회 개최 횟수'
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

        # 컬럼명 정규화 (앞뒤 공백 제거)
        df.columns = df.columns.str.strip()

        # 필수 컬럼 검증
        missing_columns = set(cls.REQUIRED_COLUMNS) - set(df.columns)
        if missing_columns:
            raise ValueError(f"필수 컬럼이 누락되었습니다: {', '.join(missing_columns)}")

        # 데이터 파싱
        parsed_data = []
        for idx, row in df.iterrows():
            try:
                data = {
                    'evaluation_year': int(row['평가년도']),
                    'college': str(row['단과대학']).strip(),
                    'department': str(row['학과']).strip(),
                    'employment_rate': Decimal(str(row['졸업생 취업률 (%)'])),
                    'full_time_faculty': int(row['전임교원 수 (명)']),
                    'visiting_faculty': int(row['초빙교원 수 (명)']),
                    'tech_transfer_income': Decimal(str(row['연간 기술이전 수입액 (억원)'])),
                    'intl_conferences': int(row['국제학술대회 개최 횟수'])
                }
                parsed_data.append(data)
            except (ValueError, KeyError, TypeError) as e:
                raise ValueError(f"{idx + 2}행 파싱 오류: {str(e)}")

        return parsed_data
