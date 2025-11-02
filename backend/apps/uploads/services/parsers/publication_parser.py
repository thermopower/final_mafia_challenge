# -*- coding: utf-8 -*-
"""
Publication CSV Parser

논문 목록 CSV 파일 파싱
"""
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime
import pandas as pd


class PublicationParser:
    """
    논문 목록 CSV 파서

    CSV 구조:
        논문ID, 게재일, 단과대학, 학과, 논문제목, 주저자, 참여저자,
        학술지명, 저널등급, Impact Factor, 과제연계여부
    """

    REQUIRED_COLUMNS = [
        '논문ID',
        '게재일',
        '단과대학',
        '학과',
        '논문제목',
        '주저자',
        '참여저자',
        '학술지명',
        '저널등급',
        'Impact Factor',
        '과제연계여부'
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
                # 게재일 파싱 (YYYY-MM-DD 형식)
                publication_date = pd.to_datetime(row['게재일']).date()

                # Impact Factor 처리 (KCI는 NULL 허용)
                impact_factor_str = str(row['Impact Factor']).strip()
                if pd.isna(row['Impact Factor']) or impact_factor_str == '' or impact_factor_str.lower() == 'nan':
                    impact_factor = None
                else:
                    impact_factor = Decimal(impact_factor_str)

                # 참여저자 처리 (빈 값 허용)
                co_authors = str(row['참여저자']).strip() if pd.notna(row['참여저자']) else ''

                data = {
                    'paper_id': str(row['논문ID']).strip(),
                    'publication_date': publication_date,
                    'college': str(row['단과대학']).strip(),
                    'department': str(row['학과']).strip(),
                    'paper_title': str(row['논문제목']).strip(),
                    'lead_author': str(row['주저자']).strip(),
                    'co_authors': co_authors,
                    'journal_name': str(row['학술지명']).strip(),
                    'journal_grade': str(row['저널등급']).strip().upper(),
                    'impact_factor': impact_factor,
                    'project_linked': str(row['과제연계여부']).strip().upper()
                }
                parsed_data.append(data)
            except (ValueError, KeyError, TypeError) as e:
                raise ValueError(f"{idx + 2}행 파싱 오류: {str(e)}")

        return parsed_data
