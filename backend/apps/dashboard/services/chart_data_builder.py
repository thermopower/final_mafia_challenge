# -*- coding: utf-8 -*-
"""
Chart Data Builder

차트 데이터 생성 로직
"""
from typing import List, Dict, Any


class ChartDataBuilder:
    """
    차트 데이터 빌더

    Backend 데이터를 Frontend 차트 형식으로 변환합니다.
    """

    @staticmethod
    def build_department_employment_rate(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        학과별 취업률 막대 그래프 데이터 생성

        Args:
            data: [{'department': '컴퓨터공학과', 'employment_rate': Decimal('87.5')}, ...]

        Returns:
            List[Dict]: [{"department": "컴퓨터공학과", "rate": 87.5}, ...]
        """
        return [
            {
                'department': item['department'],
                'rate': float(item['employment_rate'])
            }
            for item in data
        ]

    @staticmethod
    def build_faculty_trend(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        연도별 교원 수 추이 라인 차트 데이터 생성

        Args:
            data: [
                {
                    'evaluation_year': 2024,
                    'total_full_time_faculty': 150,
                    'total_visiting_faculty': 30
                },
                ...
            ]

        Returns:
            List[Dict]: [{"year": 2024, "full_time": 150, "visiting": 30}, ...]
        """
        return [
            {
                'year': item['evaluation_year'],
                'full_time': item['total_full_time_faculty'] or 0,
                'visiting': item['total_visiting_faculty'] or 0
            }
            for item in data
        ]

    @staticmethod
    def build_tech_transfer_trend(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        기술이전 수입액 추이 라인 차트 데이터 생성

        Args:
            data: [{'evaluation_year': 2024, 'total_tech_transfer_income': Decimal('120.0')}, ...]

        Returns:
            List[Dict]: [{"year": 2024, "income": 120.0}, ...]
        """
        return [
            {
                'year': item['evaluation_year'],
                'income': float(item['total_tech_transfer_income'] or 0)
            }
            for item in data
        ]

    @staticmethod
    def build_paper_distribution(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        SCIE/KCI 논문 분포 파이 차트 데이터 생성

        Args:
            data: [{'journal_grade': 'SCIE', 'count': 30}, ...]

        Returns:
            List[Dict]: [{"grade": "SCIE", "count": 30}, ...]
        """
        return [
            {
                'grade': item['journal_grade'],
                'count': item['count']
            }
            for item in data
        ]

    @staticmethod
    def build_papers_by_department(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        학과별 논문 수 막대 그래프 데이터 생성

        Args:
            data: [{'department': '컴퓨터공학과', 'count': 10}, ...]

        Returns:
            List[Dict]: [{"department": "컴퓨터공학과", "count": 10}, ...]
        """
        return [
            {
                'department': item['department'],
                'count': item['count']
            }
            for item in data
        ]

    @staticmethod
    def build_students_by_program(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        과정별 학생 수 파이 차트 데이터 생성

        Args:
            data: [{'program_type': '학사', 'count': 280}, ...]

        Returns:
            List[Dict]: [{"program": "학사", "count": 280}, ...]
        """
        return [
            {
                'program': item['program_type'],
                'count': item['count']
            }
            for item in data
        ]

    @staticmethod
    def build_students_by_department(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        학과별 학생 수 막대 그래프 데이터 생성

        Args:
            data: [{'department': '컴퓨터공학과', 'count': 80}, ...]

        Returns:
            List[Dict]: [{"department": "컴퓨터공학과", "count": 80}, ...]
        """
        return [
            {
                'department': item['department'],
                'count': item['count']
            }
            for item in data
        ]

    @staticmethod
    def build_budget_by_item(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        집행 항목별 예산 파이 차트 데이터 생성

        Args:
            data: [{'execution_item': '연구장비 도입', 'total_amount': 150000000}, ...]

        Returns:
            List[Dict]: [{"item": "연구장비 도입", "amount": 150000000}, ...]
        """
        return [
            {
                'item': item['execution_item'],
                'amount': item['total_amount']
            }
            for item in data
        ]

    @staticmethod
    def build_budget_by_funder(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        지원 기관별 연구비 막대 그래프 데이터 생성

        Args:
            data: [{'funding_agency': '한국연구재단', 'total_budget': 500000000}, ...]

        Returns:
            List[Dict]: [{"funder": "한국연구재단", "amount": 500000000}, ...]
        """
        return [
            {
                'funder': item['funding_agency'],
                'amount': item['total_budget']
            }
            for item in data
        ]
