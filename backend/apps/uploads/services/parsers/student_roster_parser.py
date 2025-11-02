# -*- coding: utf-8 -*-
"""
Student Roster CSV Parser

학생 명단 CSV 파일 파싱
"""
from typing import List, Dict, Optional
import pandas as pd


class StudentRosterParser:
    """
    학생 명단 CSV 파서

    CSV 구조:
        학번, 이름, 단과대학, 학과, 학년, 과정구분, 학적상태,
        성별, 입학년도, 지도교수, 이메일
    """

    REQUIRED_COLUMNS = [
        '학번',
        '이름',
        '단과대학',
        '학과',
        '학년',
        '과정구분',
        '학적상태',
        '성별',
        '입학년도',
        '지도교수',
        '이메일'
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
                # 지도교수 처리 (빈 값 허용)
                advisor_str = str(row['지도교수']).strip() if pd.notna(row['지도교수']) else ''
                advisor = advisor_str if advisor_str and advisor_str.lower() != 'nan' else None

                data = {
                    'student_id': str(row['학번']).strip(),
                    'name': str(row['이름']).strip(),
                    'college': str(row['단과대학']).strip(),
                    'department': str(row['학과']).strip(),
                    'grade': int(row['학년']),
                    'program_type': str(row['과정구분']).strip(),
                    'enrollment_status': str(row['학적상태']).strip(),
                    'gender': str(row['성별']).strip(),
                    'admission_year': int(row['입학년도']),
                    'advisor': advisor,
                    'email': str(row['이메일']).strip()
                }
                parsed_data.append(data)
            except (ValueError, KeyError, TypeError) as e:
                raise ValueError(f"{idx + 2}행 파싱 오류: {str(e)}")

        return parsed_data
